class FeatureMasking(tf.keras.layers.Layer):
    def __init__(self, num_features, **kwargs):
        super(FeatureMasking, self).__init__(**kwargs)
        self.num_features = num_features
        self.mask = self.add_weight("mask", (num_features,), trainable=True, initializer="ones")

    def call(self, inputs):
        return inputs * self.mask


class BinaryThreshold(Layer):
    def __init__(self, threshold=0.5, **kwargs):
        super(BinaryThreshold, self).__init__(**kwargs)
        self.threshold = threshold

    def call(self, inputs):
        return tf.where(inputs >= self.threshold, 1.0, 0.0)

    def get_config(self):
        config = super(BinaryThreshold, self).get_config()
        config.update({"threshold": self.threshold})
        return config


def custom_loss(y_true, y_pred):
    # Standard binary cross-entropy loss
    bce = tf.keras.losses.binary_crossentropy(y_true, y_pred)

    # Convert y_pred to binary (0 or 1) using TensorFlow operations
    y_pred_binary = tf.cast(y_pred > 0.5, tf.float32)

    # Calculate the sum of incorrect predictions
    incorrect_predictions = tf.abs(y_true - y_pred_binary)
    incorrect_sum = tf.reduce_sum(incorrect_predictions, axis=1)

    # Apply a penalty factor
    penalty_factor = tf.cast(incorrect_sum, tf.float32)
    penalty = tf.where(penalty_factor > 1.0, penalty_factor, 1.0)

    # Combine standard loss with additional penalty
    return bce * tf.sqrt(penalty)


def lr_schedule(epoch):
    initial_lr = 0.1  # Initial learning rate
    decay_factor = 0.1  # Factor by which to decay the learning rate
    decay_epochs = 10  # Number of epochs after which to decay the learning rate

    if epoch < decay_epochs:
        return initial_lr
    else:
        return initial_lr * decay_factor


def custom_loss_with_masking(y_true, y_pred):
    # Identify the masked rows (where all values in the row are -1)
    mask = tf.reduce_all(tf.equal(y_true, -1), axis=-1)

    # Standard binary cross-entropy loss
    bce = tf.keras.losses.binary_crossentropy(y_true, y_pred)

    # Apply the mask: Set loss to 0 for masked rows
    masked_bce = tf.where(mask, 0.0, bce)

    # Convert y_pred to binary (0 or 1) using TensorFlow operations
    y_pred_binary = tf.cast(y_pred > 0.5, tf.float32)

    # Calculate the sum of incorrect predictions, excluding masked rows
    incorrect_predictions = tf.abs(y_true - y_pred_binary)
    incorrect_sum = tf.reduce_sum(incorrect_predictions, axis=1)
    masked_incorrect_sum = tf.where(mask, 0.0, incorrect_sum)

    # Apply a penalty factor, excluding masked rows
    penalty_factor = tf.cast(masked_incorrect_sum, tf.float32)
    penalty = tf.where(penalty_factor > 1.0, penalty_factor, 1.0)

    # Combine masked standard loss with additional penalty
    combined_loss = masked_bce * tf.sqrt(penalty)

    # Compute the mean loss, excluding the masked rows
    return combined_loss


# return tf.reduce_sum(combined_loss) / tf.reduce_sum(tf.cast(~mask, tf.float32))


def custom_binary_accuracy(y_true, y_pred):
    # Mask to identify valid labels (not -1)
    valid_labels_mask = tf.not_equal(y_true, -1)

    # Apply mask to keep only valid labels and predictions
    valid_y_true = tf.boolean_mask(y_true, valid_labels_mask)
    valid_y_pred = tf.boolean_mask(y_pred, valid_labels_mask)

    # Use Keras' built-in binary_accuracy function on valid labels and predictions
    return tf.keras.metrics.binary_accuracy(valid_y_true, valid_y_pred)