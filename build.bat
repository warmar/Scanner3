cd src
pyinstaller __main__.py --windowed --noconfirm --onefile --name="Scanner3" --icon="%cd%/Resources/Icon.ico" --distpath="../distwin" --workpath="../distwin/temp" --specpath="../distwin/temp/" --hidden-import=queue
rmdir "../distwin/temp" /s /q
cd ..
pause