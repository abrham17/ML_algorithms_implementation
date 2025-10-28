; Helper function to add the first element to a subset
(= (add-first $first $subset)
  (cons-atom $first $subset))

; Power set function
(= (power-set $set)
  (if (== $set ())
    ()  ; Base case
    (let* (($first (car-atom $set))
           ($rest (cdr-atom $set))
           ($subsets-rest (power-set $rest)))
      
        (map-atom $subsets-rest $x (add-first $first $x)))))

; Example usage
!(power-set (A B C))