import os
import sys
import numpy as np
def load_CIFAR_batch(filename):
    """
    cifar-10数据集是分batch存储的，这是载入单个batch
    @参数 filename: cifar文件名
    @r返回值: X, Y: cifar batch中的 data 和 labels
    """
    with open(filename, 'r') as f:
        datadict=pickle.load(f)
        X=datadict['data']
        Y=datadict['labels']
        X=X.reshape(10000, 3, 32, 32).transpose(0,2,3,1).astype("float")
        Y=np.array(Y)
        return X, Y
def load_CIFAR10(ROOT):
    """
    读取载入整个 CIFAR-10 数据集
    @参数 ROOT: 根目录名
    @return: X_train, Y_train: 训练集 data 和 labels
             X_test, Y_test: 测试集 data 和 labels
    """
    xs=[]
    ys=[]
    for b in range(1,6):
        f=os.path.join(ROOT, "data_batch_%d" % (b, ))
        X, Y=load_CIFAR_batch(f)
        xs.append(X)
        ys.append(Y)
    X_train=np.concatenate(xs)
    Y_train=np.concatenate(ys)
    del X, Y
    X_test, Y_test=load_CIFAR_batch(os.path.join(ROOT, "test_batch"))
    return X_train, Y_train, X_test, Y_test
# 载入训练和测试数据集
X_train, Y_train, X_test, Y_test = load_CIFAR10('data/cifar10/') 
# 把32*32*3的多维数组展平
Xtr_rows = X_train.reshape(X_train.shape[0], 32 * 32 * 3) # Xtr_rows : 50000 x 3072
Xte_rows = X_test.reshape(X_test.shape[0], 32 * 32 * 3) # Xte_rows : 10000 x 3072






class NearestNeighbor:
  def __init__(self):
    pass
  def train(self, X, y):
    """ 
    这个地方的训练其实就是把所有的已有图片读取进来 -_-||
    """
    # the nearest neighbor classifier simply remembers all the training data
    self.Xtr = X
    self.ytr = y
  def predict(self, X):
    """ 
    所谓的预测过程其实就是扫描所有训练集中的图片，计算距离，取最小的距离对应图片的类目
    """
    num_test = X.shape[0]
    # 要保证维度一致哦
    Ypred = np.zeros(num_test, dtype = self.ytr.dtype)
    # 把训练集扫一遍 -_-||
    for i in xrange(num_test):
      # 计算l1距离，并找到最近的图片
      distances = np.sum(np.abs(self.Xtr - X[i,:]), axis = 1)
      min_index = np.argmin(distances) # 取最近图片的下标
      Ypred[i] = self.ytr[min_index] # 记录下label
    return Ypred
nn = NearestNeighbor() # 初始化一个最近邻对象
nn.train(Xtr_rows, Y_train) # 训练...其实就是读取训练集
Yte_predict = nn.predict(Xte_rows) # 预测
# 比对标准答案，计算准确率
print 'accuracy: %f' % ( np.mean(Yte_predict == Y_test) )





# 假定已经有Xtr_rows, Ytr, Xte_rows, Yte了，其中Xtr_rows为50000*3072 矩阵
Xval_rows = Xtr_rows[:1000, :] # 构建1000的交叉验证集
Yval = Ytr[:1000]
Xtr_rows = Xtr_rows[1000:, :] # 保留49000的训练集
Ytr = Ytr[1000:]
# 设置一些k值，用于试验
validation_accuracies = []
for k in [1, 3, 5, 7, 10, 20, 50, 100]:
  # 初始化对象
  nn = NearestNeighbor()
  nn.train(Xtr_rows, Ytr)
  # 修改一下predict函数，接受 k 作为参数
  Yval_predict = nn.predict(Xval_rows, k = k)
  acc = np.mean(Yval_predict == Yval)
  print 'accuracy: %f' % (acc,)
  # 输出结果
  validation_accuracies.append((k, acc))
