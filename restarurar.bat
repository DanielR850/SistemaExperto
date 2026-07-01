@echo off
echo =====================================
echo CLONANDO EL PROYECTO DESDE GITHUB...
echo =====================================
git clone -b version1 https://github.com/DanielR850/SistemaExperto.git
cd SistemaExperto

echo =====================================
echo CREANDO ENTORNO VIRTUAL...
echo =====================================
python -m venv venv

echo =====================================
echo ACTIVANDO ENTORNO E INSTALANDO DEPENDENCIAS...
echo =====================================
call venv\Scripts\activate
pip install -r requirements.txt

echo =====================================
echo TODO LISTO. Presiona una tecla para salir.
echo =====================================
pause
