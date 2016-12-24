Pelican でブログ その２
#######################

:date: 2016-12-23 21:59
:slug: my-first-article2
:tags: math
:summary: test
:related_posts: slug1

これは reStructuredText 形式です。その２

インライン数式は :math:`A_\text{c} = (\pi/4) d^2` てな感じに書ける。

ブロック数式の書き方は

.. math::

  \alpha_t(i) = P(O_1, O_2, \cdots O_t, q_t= S_i \lambda)

  \newcommand\T{\Rule{0pt}{1em}{.3em}}
  \begin{array}{ll} 
  最大化 & 2x_{1}+x_{2}~~~~~~~~~~~・・・・・・利益(式1)\\ 
  条件式 & \left\{ 
  \begin{array}{lll} 
  &x_{1}+2x_{2} \leq 10~~・・・・・・材料1の使用条件(式2)\\ 
  &x_{1}+x_{2} \leq 6~~~~~~・・・・・・材料2の使用条件(式3)\\ 
  &3x_{1}+x_{2} \leq 12~~・・・・・・材料3の使用条件(式4)\\ 
  &x_{1}，x_{2} \geq 0\\     
  \end{array} 
  \right . 
  \end{array}


.. math::
  \newcommand\T{\Rule{0pt}{1em}{.3em}}
	\begin{array}{|c|c|}
	\hline X & P(X = i) \T \\\hline
	  1 \T & 1/6 \\\hline
	  2 \T & 1/6 \\\hline
	  3 \T & 1/6 \\\hline
	  4 \T & 1/6 \\\hline
	  5 \T & 1/6 \\\hline
	  6 \T & 1/6 \\\hline
	\end{array}

数式テスト