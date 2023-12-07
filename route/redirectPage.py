

from flask import redirect, render_template, session, url_for
from utilities import utilities







def redirectPage(target, message):
    session['target'] = target
    session['message'] = message
    if target == "/login":
        return render_template('transition.html', target="/login", message = message)
    elif target == "/logout":
        return render_template('transition.html', target="/login", message = "The token has expired, please log in again!")
    elif target == "/adminTool":
        return render_template('transition.html', target="/adminTool", message = message)
    elif target == "redirectBack":
        return render_template('transition.html', target="redirectBack", message = message)
    else:
        return redirect(url_for('home'))