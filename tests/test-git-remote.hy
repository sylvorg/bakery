(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(import pytest [mark])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :key True))
(import bakery [git])
(import shutil [which])
(defn [mark.git-remote (.skipif mark (not (which "git")) :reason "Git may not be available on some systems")]
      test-git-status [request] (-> (git :C request.config.rootdir) (.remote :m/str True) (= "origin") assert))
