"""Flask site for Balloonicorn's Party."""

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


def is_mel(name, email):
    """Is this user Mel?

    >>> is_mel('Mel Melitpolski', 'mel@ubermelon.com')
    True
    >>> is_mel('Mel', 'mel@ubermelon.com')
    True
    >>> is_mel('MEL MELITPOLSKI', 'mel@ubermelon.com')
    True
    >>> is_mel('Ann Star', 'ann@ubermelon.com')
    False
    """
    return name.lower() == "mel melitpolski" or email.lower() == "mel@ubermelon.com" or name.upper() == "MEL MELITPOLSKI" or email == "MEL@UBERMELON.COM" or name == "Mel Melitpolski" or email == "mel@ubermelon.com"
        
    #return name == "Mel Melitpolski" or email == "mel@ubermelon.com"
    

def most_and_least_common_type(treats):
    """Given list of treats, return most and least common treat types.

    Return most and least common treat types in tuple of format (most, least).
    
    # treats=[{'type': 'ice_cream'},{'type': 'cake'},{'type': 'ice_cream'},{'type': 'dessert'}]
    >>> most_and_least_common_type(treats=get_treats())
    ('dessert', 'drink')

    >>> treats =[{'type':'chocolate'}, {'type': 'chocolate'}]
    >>> most_and_least_common_type (treats)
    ('chocolate', 'chocolate')

     >>> treats =[]
    >>> most_and_least_common_type (treats)
    (None, None)
    """

    types = {}

    # Count number of each type
    #print('TREATS=', treats)
    for treat in treats:
        types[treat['type']] = types.get(treat['type'], 0) + 1

    most_count = most_type = None
    least_count = least_type = None

    # Find most, least common
    for treat_type, count in types.items():
        if most_count is None or count > most_count:
            most_count = count
            most_type = treat_type

        if least_count is None or count < least_count:
            least_count = count
            least_type = treat_type
    #print((most_type, least_type))
    return (most_type, least_type)


def get_treats():
    """Return treats being brought to the party.

    One day, I'll move this into a database! -- Balloonicorn
    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Leslie'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Bonnie'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'Katie'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Anges'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Henry'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Sarah'}
    ]


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/treats")
def show_treats():
    """Show treats people are bringing."""

    treats = get_treats()

    most, least = most_and_least_common_type(get_treats())

    return render_template("treats.html",
                           treats=treats,
                           most=most,
                           least=least)


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    if not is_mel(name, email):
        session['rsvp'] = True
        flash("Yay!")
        return redirect("/")

    else:
        flash("Sorry, Mel. This is kind of awkward.")
        return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
