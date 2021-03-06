#!/bin/bash
urls=(
    https://www.deeplearningbook.org/contents/TOC.html
    https://www.deeplearningbook.org/contents/acknowledgements.html
    https://www.deeplearningbook.org/contents/notation.html
    https://www.deeplearningbook.org/contents/intro.html
    https://www.deeplearningbook.org/contents/part_basics.html
    https://www.deeplearningbook.org/contents/linear_algebra.html
    https://www.deeplearningbook.org/contents/prob.html
    https://www.deeplearningbook.org/contents/numerical.html
    https://www.deeplearningbook.org/contents/ml.html
    https://www.deeplearningbook.org/contents/part_practical.html
    https://www.deeplearningbook.org/contents/mlp.html
    https://www.deeplearningbook.org/contents/regularization.html
    https://www.deeplearningbook.org/contents/optimization.html
    https://www.deeplearningbook.org/contents/convnets.html
    https://www.deeplearningbook.org/contents/rnn.html
    https://www.deeplearningbook.org/contents/guidelines.html
    https://www.deeplearningbook.org/contents/applications.html
    https://www.deeplearningbook.org/contents/part_research.html
    https://www.deeplearningbook.org/contents/linear_factors.html
    https://www.deeplearningbook.org/contents/autoencoders.html
    https://www.deeplearningbook.org/contents/representation.html
    https://www.deeplearningbook.org/contents/graphical_models.html
    https://www.deeplearningbook.org/contents/monte_carlo.html
    https://www.deeplearningbook.org/contents/partition.html
    https://www.deeplearningbook.org/contents/inference.html
    https://www.deeplearningbook.org/contents/generative_models.html
    https://www.deeplearningbook.org/contents/bib.html
    https://www.deeplearningbook.org/contents/index-.html
)
python3 -m autowebprint ${urls[@]} -f dlbook-out -v -o prefs=ff-a4-P -o n_threads=8
