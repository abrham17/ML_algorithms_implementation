;; CMA-ES Implementation using pyModule for Python operations
!(import! &self utils)

;; Basic helpers
(= (empty? $lst) (== $lst ()))
(= (sq $x) (* $x $x))

;; Fixed zip function
(= (zip $a $b)
   (if (or (empty? $a) (empty? $b)) 
       ()
       (let* (($x (car-atom $a))
              ($xs (cdr-atom $a))
              ($y (car-atom $b))
              ($ys (cdr-atom $b))
              ($rest (zip $xs $ys)))
         (cons-atom ($x $y) $rest))))

;; Range function using proper recursion
(= (range $start $end)
  (if (> $start $end) ()
    (let* (($incre (+ $start 1))
            ($range (range $incre $end)))
      (cons-atom $start $range)
    )
  )
)
;; Repeat function
(= (repeat $item $k)
  (if (== $k 0) ()
    (let* (($result (repeat $item (- $k 1))))
      (cons-atom $item $result)
    )
  )
)

;; Vector operations
(= (zero-vec $dim) (repeat 0 $dim))
(= (zero-mat $dim) (repeat (zero-vec $dim) $dim))

(= (vec-add $a $b)
  (if (or (empty? $a) (empty? $b)) ()
      (let* (($first_a (car-atom $a))
             ($first_b (car-atom $b))
             ($rest_a (cdr-atom $a))
             ($rest_b (cdr-atom $b))
             ($ans (+ $first_a $first_b))
             ($rest (vec-add $rest_a $rest_b)))
        (cons-atom $ans $rest))))

;; Vector subtraction
(= (vec-sub $a $b)
  (if (or (empty? $a) (empty? $b)) ()
      (let* (($first_a (car-atom $a))
             ($first_b (car-atom $b))
             ($rest_a (cdr-atom $a))
             ($rest_b (cdr-atom $b))
             ($ans (- $first_a $first_b))
             ($rest (vec-sub $rest_a $rest_b)))
        (cons-atom $ans $rest))))

;; Vector scaling - simplified version

(= (vec-scale $s $v)
  (map-atom $v $x (* $s $x))
)

;; Matrix operations
(= (mat-scale $s $m)
  (map-atom $m $row (vec-scale $s $row))
)


;; Matrix addition
(= (mat-add $a $b)
  (if (or (empty? $a) (empty? $b)) ()
      (let* (($first_a (car-atom $a))
             ($first_b (car-atom $b))
             ($rest_a (cdr-atom $a))
             ($rest_b (cdr-atom $b))
             ($ans (vec-add $first_a $first_b))
             ($rest (mat-add $rest_a $rest_b)))
        (cons-atom $ans $rest))))

;; Clamping function for bounds [0,1]
(= (clamp $x)
  (if (< $x 0) 0
    (if (> $x 1) 1 $x)
  )
)

(= (clamp-vec $v)
  (map-atom $v $ele (clamp $ele))
)

;; Norm calculation
(= (norm $v)
  (sqrt-math (foldl-atom $v 0 $acc $x (+ $acc (* $x $x))))
)

;; Take function
(= (take $k $lst)
  (if (or (== $k 0) (empty? $lst)) ()
    (let* (($rest-expr (cdr-atom $lst))
           ($first (car-atom $lst))
           ($rest (take (- $k 1) $rest-expr))
            )
      (cons-atom $first $rest)
    )
  )
)

;; CMA-ES parameters
(= (n) 5)
(= (lambda) 10)
(= (mu) 5)

;; Population generation using pyModule
(= (gen-pop $mean $sigma $cov $num)
  (if (== $num 0) ()
    (let* (($sample (pyModuleX py_multivariate_normal ($mean $cov $sigma)))
            ($clamped-sample (clamp-vec $sample))
            ($pop (gen-pop $mean $sigma $cov (- $num 1)))
            )
      (cons-atom $clamped-sample $pop)
    )
  )
)



;; Matrix operations using pyModule
(= (outer-product $v1 $v2)
  (pyModuleX outer-product ($v1 $v2))
)

(= (mat-mul $mat $vec)
  (pyModuleX mat-mul ($mat $vec))
)

(= (inv-sqrt $mat)
  (pyModuleX inv-sqrt ($mat))
)

(= (identity-matrix $n)
  (pyModule identity-matrix $n)
)
(= (find-best $pop $new-pop $fits $i $best-index $min-fit)
  (if (empty? $fits)
    (index-atom $pop $best-index)
    (let* (
        ($current-fit (car-atom $fits))
        ($new-best (if (< $current-fit $min-fit) $i $best-index))
        ($new-min (if (< $current-fit $min-fit) $current-fit $min-fit))
        (() (println! ("new-min" $new-min "$new-best" $new-best)))
        ($rest-pop (cdr-atom $new-pop))
        (() (println! ("rest-pop" $rest-pop) ))
        ($rest-fit (cdr-atom $fits))
        (() (println! ("rest-fit" $rest-fit) ))

        ($new-i (+ $i 1))
      )
      (find-best $pop $rest-pop $rest-fit $new-i $new-best $new-min)
    )
  )
)
;; Simple CMA-ES implementation
(= (simple-cma-es-iter $mean $sigma $cov $best-w $best-fit $gen $max-gen $pop-size)
  (if (>= $gen $max-gen)
    $best-w
    (let* (
        ;; Generate population
        ($pop (gen-pop $mean $sigma $cov $pop-size))
        (() (println! ("gen-pop" $pop)) )
        ;; Evaluate fitness
        ($fits (map-atom $pop $x (pyModule py_fitness $x)))
        (() (println! ("new-best-w" $fits)))

        ;; Find best individual
        ($best-index 0)
        ($min-fit (min-atom $fits))
        ($new-best-w (find-best $pop $pop $fits 0 0 $min-fit))
        (() (println! ("new-best-w" $new-best-w)))

        ($new-best-fit   (pyModuleX py_fitness ($new-best-w)))
        (() (println! ("new-best-fit" $new-best-fit)))
        ;; Update mean (simple average)
        ($new-mean (vec-scale (/ 1 $pop-size) 
                   (foldl-atom $pop (zero-vec (n)) $acc $x (vec-add $acc $x))))
        
        ;; Update best solution
        ($final-best-w (if (< $new-best-fit $best-fit) $new-best-w $best-w))
        ($final-best-fit (if (< $new-best-fit $best-fit) $new-best-fit $best-fit))
        (() (println! (concat "Generation " $gen ": Best fitness = " $final-best-fit)))

      )
      (simple-cma-es-iter $new-mean $sigma $cov $final-best-w $final-best-fit (+ $gen 1) $max-gen $pop-size)
    )
  )
)


(= (simple-cma-es $pop-size $max-gen)
  (let* (
      ($mean (zero-vec (n)))
      (() (println! ("Starting CMA-ES Optimization" $mean)))
      ($sigma 0.5)
      (() (println! ("Starting CMA-ES Optimization" $sigma)))
      ($cov   (pyModuleX identity_matrix (5)))
      (() (println! ("Starting CMA-ES Optimization" $cov)))
      ($best-w $mean)
      ($best-fit (pyModuleX py_fitness $mean))
      (() (println! ("Best Fit" $best-fit)))
      ($gen 0)
    )
    (simple-cma-es-iter $mean $sigma $cov $best-w $best-fit $gen $max-gen $pop-size)
  )
)





!(simple-cma-es 20 50)
