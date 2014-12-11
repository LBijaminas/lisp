(defun my_max (x y)
	(cond 
		;; if the param passed is not an integer, return nil
		((or (not (integerp x)) (not (integerp y))) nil)
		((> x y) x)
		(t y)
	)
)

(defun find_max (lst)
	(cond
		;; list can only contain integers. otherwise, it will return nil, as defined in my_max
		((not (listp lst)) nil)
		((equalp (length lst) 1) (car lst))
		(t (my_max (car lst) (find_max (cdr lst))))
	)
)


(defun get_count (lst)
	(cond
		;; firstly, it has to be a list
		((not (listp lst)) nil)

		;; for empty list, count is 0
		((equal lst nil) 0)
		
		;; if the element is a list, return the count inside that list and add it to recursion on cdr
		((listp (car lst)) (+ (get_count (car lst)) (get_count (cdr lst))))

		;; if the element is the last element of the list (but it is not a list), return 1
		((equalp (length lst) 1) 1)

		;; if the element  is not a list, just add 1
		(t (+ 1 (get_count (cdr lst))))
	)
)