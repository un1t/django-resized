{ pkgs ? import <nixpkgs> {
} }:
let 
  python_dependencies = with pkgs.python39Packages; [
    coverage flake8 coveralls pillow django
  ];
  python_resized = pkgs.python39.buildEnv.override {
    extraLibs = python_dependencies;
  };
in pkgs.mkShell {
  buildInputs = [ python_resized ];
  shellHook = ''
    export PIP_PREFIX=$(pwd)/_build/pip_packages
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    unset SOURCE_DATE_EPOCH

    pip install -e .

    alias flake8="${python_resized}/bin/python -m flake8 --ignore=E501,W504 django_resized"
    alias test="${python_resized}/bin/python -m coverage run `which django-admin` test --settings=django_resized.tests.settings"
  '';
}