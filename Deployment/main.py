from website import create_app

app = create_app()

if __name__ == '__main__': # only if we run this file, we will execute this line
    app.run(debug = True) # everytime that we make a change to our python code, it will automatically rerun the webserver
