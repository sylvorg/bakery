(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :sort True))
(defn test-false-error [] (-> (ls :j True :m/false-error True) (not) (assert)))
(defn test-replace-error []
      (assert (ls :j True :m/replace-error True))
      (-> (ls :j True :m/replace-error "replace error test") (= "replace error test") (assert)))