from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET'])
@app.route("/home/", methods=['GET'])
def home():
	return render_template('welcome.html', nav='home')

#not found route 
# @app.errorhandler(404)
# def page_not_found(e):
# 	return render_template('404.html', title="Not Found"), 404

#https://stackoverflow.com/questions/63530652/storing-and-accessing-dictionary-data-in-flask

if __name__ == '__main__':
	app.run()