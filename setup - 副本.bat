rmdir /s /q dist
python3 .\setup.py bdist_wheel
twine upload -u coco56 -p password dist/*
git add .
git commit -m "������%date:~0,4%��%date:~5,2%��%date:~8,2%��	%time%"
git push -f origin main
timeout /t 60
pip3 install --upgrade pacc
pause