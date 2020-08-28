# A deep learning approach on fault detection and diagnosis of industrial solenoid valves

Abstract:

In manufacturing and production industries, abrupt equipment breakdowns lead
to production or manufacturing downtime. Production downtime is a costly affair.
To avoid such unanticipated downtime, it is good to adopt preventive maintenance.
Preventive maintenance involves regular inspections for fault detection in industrial
equipment and action is taken to fix the issue as soon as possible. In this work,
deep learning approaches are utilized to detect faults in industrial solenoid valves
by studying the solenoid current curves. A simple laboratory-level data collection
setup is designed to obtain the necessary data from the set of solenoid valves under
study. Solenoid current curves are obtained by operating the solenoid valves at
varying values of temperature and inlet pressures. Neural network models based
on three popular architectures namely, Fully Connected Neural Networks, Convolutional
Neural Networks and Long Short Term Memory are implemented for
classifying the solenoid valves under study into different fault classes. Two data
pre-processing techniques are proposed in this work, namely window of inflection
concept and the addition of white Gaussian noise to input data. All the neural
networks were trained with all combinations of the proposed data pre-processing
techniques. Performance metrics of the implemented neural network models under
different scenarios are bench-marked and compared. Classification accuracy
ranging from 89% to 98% was achieved with the implemented neural network
models for new unseen data. Window of inflection concept was found to improve
the performance of all neural network models implemented. Addition of Gaussian
noise improved performance of Fully Connected Neural Networks and Convolutional
Neural Networks.
