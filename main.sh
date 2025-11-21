if [ $# -gt 0 ]; then
  if [[ "$1" == "test" ]]; then
    uv run src/main.py
  elif [[ "$1" == "prod" ]]; then
    uv run src/main.py "/sitegen/"
  fi
else
  echo "No deployment option provided"
  exit 1
fi

cd docs && uv run -m http.server 8888
