from utils import generate_random_range


class NeuralBird:
    def __init__(self, param=5):
        self.distance = 0
        self.bird_height = 0
        self.pipe_bottom_height = 0
        self.pipe_top_height = 0
        self.velocity = 0
        if isinstance(param, list):
            self.weights = param.copy()
        else:
            self.weights = [generate_random_range() for _ in range(param)]

    def compute_output(self):
        result = self.distance * self.weights[0] + \
                 self.bird_height * self.weights[1] + \
                 self.pipe_bottom_height * self.weights[2] + \
                 self.pipe_top_height * self.weights[3] + \
                 self.velocity * self.weights[4]
        return result > 0

    def update_inputs(self, distance, bird_height, pipe_bottom_height, pipe_top_height, velocity):
        self.distance = distance
        self.bird_height = bird_height
        self.pipe_bottom_height = pipe_bottom_height
        self.pipe_top_height = pipe_top_height
        self.velocity = velocity

    def get_list_weights(self):
        return self.weights.copy()
