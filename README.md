Information Retrieval
============

Video Lectures
============

[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video1.jpg width="50%">](https://youtu.be/DhjZPVrvdnE)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video2.jpg width="50%">](https://youtu.be/rfNoyFw-_g8)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video3.jpg width="50%">](https://youtu.be/sYHVpTZL6o4)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video4.jpg width="50%">](https://youtu.be/bRckCK9VcKQ)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video5.jpg width="50%">](https://youtu.be/ZX4zTT69ll0)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video6.jpg width="50%">](https://youtu.be/AVoLka-LDXY)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video7.jpg width="50%">](https://youtu.be/5GOyBTeSJwo)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video8.jpg width="50%">](https://youtu.be/-iu6N8KZslw)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video9.jpg width="50%">](https://youtu.be/LwQYHFyDd8U)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video10.jpg width="50%">](https://youtu.be/Y_jS03r6GMI)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video11.jpg width="50%">](https://youtu.be/msRT2yx0yms)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video12.jpg width="50%">](https://youtu.be/B5RProYhMvk)[<img src=https://github.com/StarlangSoftware/InformationRetrieval/blob/master/video13.jpg width="50%">](https://youtu.be/dxc3ONoW63E)

For Developers
============

You can also see [Java](https://github.com/starlangsoftware/InformationRetrieval), [Cython](https://github.com/starlangsoftware/InformationRetrieval-Cy), [C++](https://github.com/starlangsoftware/InformationRetrieval-CPP), [Js](https://github.com/starlangsoftware/InformationRetrieval-Js), [C](https://github.com/starlangsoftware/InformationRetrieval-C), or [C#](https://github.com/starlangsoftware/InformationRetrieval-CS) repository.

For Contibutors
============

### Setup.py file
1. Do not forget to set package list. All subfolders should be added to the package list.
```
    packages=['Classification', 'Classification.Model', 'Classification.Model.DecisionTree',
              'Classification.Model.Ensemble', 'Classification.Model.NeuralNetwork',
              'Classification.Model.NonParametric', 'Classification.Model.Parametric',
              'Classification.Filter', 'Classification.DataSet', 'Classification.Instance', 'Classification.Attribute',
              'Classification.Parameter', 'Classification.Experiment',
              'Classification.Performance', 'Classification.InstanceList', 'Classification.DistanceMetric',
              'Classification.StatisticalTest', 'Classification.FeatureSelection'],
```
2. Package name should be lowercase and only may include _ character.
```
    name='nlptoolkit_math',
```

### Python files
1. Do not forget to comment each function.
```
    def __broadcast_shape(self, shape1: Tuple[int, ...], shape2: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Determines the broadcasted shape of two tensors.

        :param shape1: Tuple representing the first tensor shape.
        :param shape2: Tuple representing the second tensor shape.
        :return: Tuple representing the broadcasted shape.
        """
```
2. Function names should follow caml case.
```
    def addItem(self, item: str):
```
3. Local variables should follow snake case.
```
	det = 1.0
	copy_of_matrix = copy.deepcopy(self)
```
4. Class variables should be declared in each file.
```
class Eigenvector(Vector):
    eigenvalue: float
```
5. Variable types should be defined for function parameters and class variables.
```
    def getIndex(self, item: str) -> int:
```
6. For abstract methods, use ABC package and declare them with @abstractmethod.
```
    @abstractmethod
    def train(self, train_set: list[Tensor]):
        pass
```
7. For private methods, use __ as prefix in their names.
```
    def __infer_shape(self, data: Union[List, List[List], List[List[List]]]) -> Tuple[int, ...]:
```
8. For private class variables, use __ as prefix in their names.
```
class Matrix(object):
    __row: int
    __col: int
    __values: list[list[float]]
```
9. Write \_\_repr\_\_ class methods as toString methods
10. Write getter and setter class methods.
```
    def getOptimizer(self) -> Optimizer:
        return self.optimizer
    def setValue(self, value: Optional[Tensor]) -> None:
        self._value = value
```
11. If there are multiple constructors for a class, define them as constructor1, constructor2, ..., then from the original constructor call these methods.
```
    def constructor1(self):
        self.__values = []
        self.__size = 0

    def constructor2(self, values: list):
        self.__values = values.copy()
        self.__size = len(values)

    def __init__(self,
                 valuesOrSize=None,
                 initial=None):
        if valuesOrSize is None:
            self.constructor1()
        elif isinstance(valuesOrSize, list):
            self.constructor2(valuesOrSize)
```
12. Extend test classes from unittest and use separate unit test methods.
```
class TensorTest(unittest.TestCase):

    def test_inferred_shape(self):
        a = Tensor([[1.0, 2.0], [3.0, 4.0]])
        self.assertEqual((2, 2), a.getShape())

    def test_shape(self):
        a = Tensor([1.0, 2.0, 3.0])
        self.assertEqual((3, ), a.getShape())
```
13. Enumerated types should be used when necessary as enum classes.
```
class AttributeType(Enum):
    """
    Continuous Attribute
    """
    CONTINUOUS = auto()
    """
    Discrete Attribute
    """
    DISCRETE = auto()
```
