rmdir /s /q dist
python .\setup.py bdist_wheel
twine upload -u coco56 -p password dist/*
git add .
git commit -m "更新于%date:~0,4%年%date:~5,2%月%date:~8,2%日	%time%"
git push -f origin main
python -m pip install --upgrade pip
pip install --upgrade pacc
timeout /t 15
pip install --upgrade pacc
pause