# What's this?

Experimental tools to get you from python functions to a browser based dashboard exhibiting these: That is, allowing you to 
see these functions, select one, see the signature, enter the inputs, call the function, and see the results.

At the time of writing this, it's only a proof of concept. 
Still, it works perfectly if your functions only have simple types (or you wrapped them with input/output converting layers), and you're okay with the default choice of layout and output format.

Yet we obviously want to do more! We want to allow the user to use any function, simply by specifying how complex types should be handled (and doing so with minimal boilerplate). We want to allow a range of possible layouts, navigation structures and output presentations.

# Example

Consider the code below:

```python

def foo(a: int = 0, b: int = 0, c=0):
    """This is foo. It computes something"""
    return (a * b) + c


def bar(x, greeting='hello'):
    """bar greets it's input"""
    return f"{greeting} {x}"


def confuser(a: int = 0, x: float = 3.14):
    return (a ** 2) * x


if __name__ == '__main__':
    from py2dash.app_makers import dispatch_funcs

    app = dispatch_funcs([foo, bar, confuser])
    app.run_server(debug=True)
```

You basically have three functions that are defined. 
The list of these functions are handed to the `dispatch_funcs` function which returns an app object. 
When you call `app.run_server()` then, a server will launch and you'll be given a default url to go to (default is `http://127.0.0.1:8050/`). 

When you go to that url, you'll first see a list of the (clickable) function names.

![alt text](img/dash_home.png)

Click on foo and you'll see `foo`'s name and signature. Enter a few numbers there, click execute, and you get:

![alt text](img/dash_foo.png)

Yep. It's alive! Try it again, try it again. Click on `bar` and do something with it...

![alt text](img/dash_bar.png)

Again!

![alt text](img/dash_confuser.png)

Convinced?
