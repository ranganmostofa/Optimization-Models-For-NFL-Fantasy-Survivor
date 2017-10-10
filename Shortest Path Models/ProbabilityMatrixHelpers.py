from math import ceil, log, exp


class ProbabilityMatrixHelpers:
    """

    """

    EPSILON = 0.01  # public static constants

    @staticmethod
    def find_matrix_min(P):
        """

        :param P:
        :return:
        """
        row_mins = list()
        for row in P:
            row_mins.append(min([element for element in row if element != 0.00]))
        return min(row_mins)

    @staticmethod
    def compute_base(P):
        """

        :param P:
        :return:
        """
        return ceil(1.00 / ProbabilityMatrixHelpers.find_matrix_min(P))

    @staticmethod
    def scale_matrix(P, scale):
        """

        :param P:
        :param scale:
        :return:
        """
        scaled_matrix = list()
        for row in P:
            scaled_row = list()
            for column in row:
                scaled_row.append(column * scale)
            scaled_matrix.append(scaled_row)
        return scaled_matrix

    @staticmethod
    def log_transform(P, base):
        """

        :param P:
        :param base:
        :return:
        """
        transformed_matrix = list()
        for row in P:
            transformed_row = list()
            for column in row:
                if not column:
                    column = 1 + ProbabilityMatrixHelpers.EPSILON
                transformed_row.append(log(column, base))
            transformed_matrix.append(transformed_row)
        return transformed_matrix

    @staticmethod
    def build_cost_matrix(P):
        """

        :param P:
        :return:
        """
        C = list()
        scaled_P = ProbabilityMatrixHelpers.scale_matrix(P, ProbabilityMatrixHelpers.compute_base(P))
        transformed_P = ProbabilityMatrixHelpers.log_transform(scaled_P, ProbabilityMatrixHelpers.compute_base(P))
        for row in transformed_P:
            C_row = list()
            for col in row:
                C_row.append(exp(1.00 / col))
            C.append(C_row)
        return C

    @staticmethod
    def flip_probability_matrix(P):
        """

        :param P:
        :return:
        """
        flipped_P = list()
        for row in P:
            flipped_row = list()
            for col in row:
                flipped_row.append(1.00 - float(col))
            flipped_P.append(flipped_row)
        return flipped_P

