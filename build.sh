cd src || exit
pyinstaller __main__.py --name="Scanner3" --icon="Resources/Icon.ico" --windowed --noconfirm --onefile --distpath="../distlinux" --workpath="../distlinux/temp" --specpath="../distlinux/temp/" --hidden-import=queue --hidden-import='PIL._tkinter_finder'
rm -rf "../distlinux/temp"
cd ..
