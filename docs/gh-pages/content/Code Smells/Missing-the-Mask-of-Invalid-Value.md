---
title: "Missing the Mask of Invalid Value"
disableShare: true
# ShowReadingTime: true
tags: ["generic", "model training", "error-prone"]
weight: 11
---

### Description

Several posts on Stack Overflow talk about the bugs that are not easy to discover caused by the log parameter approaching zero. In this kind of program, the log function variable turns to zero and raises an error during the training process. However, the error's stack trace did not directly point to the line of code that the bug exist. This kind of problem is not easy to debug and might take a long training time to find. Therefore, the developer should check the log parameter and may add a very small number to the log parameter in the code before running it. It will save time and effort if the developer could identify this smell before the code run into errors.

### Type

Generic

### Existing Stage

Model Training

### Effect

Error-prone

### Example

```diff
### TensorFlow 1.x
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
sess = tf.InteractiveSession()

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_Variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1],padding="SAME")

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1],padding="SAME")

x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])

x_image = tf.reshape(x, [-1, 28, 28, 1])

W_conv1 = weight_variable([5,5,1,32])
b_conv1 = bias_Variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5,5,32,64])
b_conv2 = bias_Variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7*7*64,1024])
b_fc1 = bias_Variable([1024])
h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

W_fc2 = weight_variable([1024,10])
b_fc2 = bias_Variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)

- cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y_conv),reduction_indices=[1]))
+ cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(tf.clip_by_value(y_conv,1e-10,1.0)),reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

tf.global_variables_initializer().run()

for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict = {x:batch[0] , y_:batch[1], keep_prob: 1.0})
        print("step %d,train accuracy %g"%(i,train_accuracy))
    train_step.run(feed_dict = {x:batch[0] , y_:batch[1], keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict = {x:mnist.test.images,y_:mnist.test.labels,keep_prob:1.0}))
```

### Source:

#### Paper 
- Nargiz Humbatova, Gunel Jahangirova, Gabriele Bavota, Vincenzo Riccio, AndreaStocco, and Paolo Tonella. 2020. Taxonomy of real faults in deep learning sys-tems. InProceedings of the ACM/IEEE 42nd International Conference on SoftwareEngineering. 1110–1121.
- Yuhao Zhang, Yifan Chen, Shing-Chi Cheung, Yingfei Xiong, and Lu Zhang. 2018.An empirical study on TensorFlow program bugs. InProceedings of the 27th ACMSIGSOFT International Symposium on Software Testing and Analysis. 129–140.

#### Grey Literature

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/33712178/tensorflow-nan-bug
- https://stackoverflow.com/questions/33699174/tensorflows-relugrad-claims-input-is-not-finite
- https://stackoverflow.com/questions/39487825/tensorflow-convolutionary-net-grayscale-vs-black-white-training
- https://stackoverflow.com/questions/35078027/implement-mlp-in-tensorflow

#### Documentation

