import tensorflow as tf

import tensor_train
from initializers import tt_rand_tensor

def get_tt_variable(name,
                    shape=None,
                    rank=None,
                    dtype=None,
                    initializer=None,
                    regularizer=None,
                    trainable=True,
                    collections=None,
                    caching_device=None,
                    validate_shape=True):
  """Returns TensorTrain object with tf.Variables as the TT-cores.

  Args:
    name: The name of the new or existing TensorTrain variable.
      Used to name the TT-cores.
    shape: Shape of the new or existing TensorTrain variable.
    rank: A positive number or a list of numbers -- TT-rank or TT-ranks for
      each core for the new or existing TensorTrain variable.
    dtype: Type of the new or existing TensorTrain variable TT-cores (defaults
      to DT_FLOAT).
    initializer: Initializer for the variable if one is created.
    regularizer: Not supported yet.
    trainable: If True also add the variable to the graph collection
      GraphKeys.TRAINABLE_VARIABLES (see tf.Variable).
    collections:  List of graph collections keys to add the Variables
      (underlying TT-cores). Defaults to [GraphKeys.GLOBAL_VARIABLES]
      (see tf.Variable).
    caching_device: Optional device string or function describing where
      the Variable should be cached for reading. Defaults to the Variable's
      device. If not None, caches on another device. Typical use is to cache
      on the device where the Ops using the Variable reside, to deduplicate
      copying through Switch and other conditional statements.
    validate_shape: If False, allows the variable to be initialized with a value
      of unknown shape. If True, the default, the shape of initial_value must be
      known.

  Returns:
    The created or existing `TensorTrain` object with tf.Variables TT-cores.

  Raises:
    `ValueError`: when creating a new variable and shape is not declared, when
      violating reuse during variable creation, or when initializer dtype and
      dtype don't match. Reuse is set inside variable_scope.
  """
  # TODO: check that if there is an initializer, rank and shape are not provided
  # by the user because they will be ignored anyway.
  # TODO: How to use get_variable(shape, rank) for TT-matrices?
  # TODO: support regularizer (a TensorTrain -> Tensor function).
  # TODO: Provide basic regularizers (like apply_to_cores(func)).
  if initializer is None:
    # TODO: if variable already exist, do not create a new initializer.
    initializer = tt_rand_tensor(shape, rank)

  num_dims = initializer.ndims()
  variable_cores = []
  # TODO: name_scope or variable_scope?
  with tf.name_scope(name):
    for i in range(num_dims):
      curr_core_var = tf.get_variable('core_%d' % i,
                                      initializer=initializer.tt_cores[i],
                                      dtype=dtype, trainable=trainable,
                                      collections=collections,
                                      caching_device=caching_device,
                                      validate_shape=validate_shape)
      variable_cores.append(curr_core_var)

  return tensor_train.TensorTrain(variable_cores, convert_to_tensors=False)

