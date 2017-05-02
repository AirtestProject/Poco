# coding=utf-8
__author__ = 'lxn3032'


class ControllerBase(object):
    def __init__(self, period, ValueType=float):
        self.ValueType = ValueType
        self.T = period
        self.error_1 = ValueType(0)
        self.error_2 = ValueType(0)
        self.current_value = ValueType(0)
        self.target_value = ValueType(0)

    def delta_closed_loop_gain(self, feedback):
        raise NotImplementedError

    def close_loop_gain(self, feedback):
        raise NotImplementedError

    def set_target_value(self, val):
        self.target_value = val

    def get_current_value(self):
        return self.current_value

    def reset_errors(self):
        self.error_1 = self.error_2 = self.ValueType(0)


class PIDController(ControllerBase):
    def __init__(self, period, Kp=1, Ki=0, Kd=0, ValueType=float):
        super(PIDController, self).__init__(period, ValueType)
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.sum_error = ValueType(0)

    def delta_closed_loop_gain(self, feedback):
        self.current_value = feedback
        error = self.target_value - self.current_value
        d_error = error - self.error_1
        d2_error = error - 2 * self.error_1 + self.error_2
        delta_output = self.Kp * d_error + self.Ki * error + self.Kd * d2_error

        self.error_2 = self.error_1
        self.error_1 = error
        return delta_output

    def closed_loop_gain(self, feedback):
        self.current_value = feedback
        error = self.target_value - self.current_value
        self.sum_error += error
        d_error = error - self.error_1
        output = self.Kp * error + self.Ki * self.sum_error + self.Kd * d_error

        self.error_2 = self.error_1
        self.error_1 = error
        return output
