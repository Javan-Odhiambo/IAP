import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description="Run django and code style tests.")
parser.add_argument("-d", "--django", action="store_true", help="run Django tests")
parser.add_argument("-s", "--style", action="store_true", help="run Code Style tests")


def _(title=""):
    """Helper to show separation between the tests"""
    if title:
        print(f"----------------- {title.upper()} -----------------")
    else:
        print("__________________________________________")


def django_tests():
    """Run django tests"""
    _("Django")
    subprocess.call([sys.executable, "manage.py", "test", "apps"])


def style_tests():
    """Perform linting and code style tests"""
    _("Black")
    subprocess.call(
        [sys.executable, "-m", "black", "--check", "--diff", "--color", "."]
    )
    _("Isort")
    subprocess.call([sys.executable, "-m", "isort", "--check", "--diff", "."])
    _("Flake8")
    subprocess.call(
        [sys.executable, "-m", "flake8", "--show-source", "--statistics", "."]
    )


def main():
    # Set environment variables temporarily for the tests
    os.environ["DEBUG"] = "True"
    os.environ["USE_SQLITE"] = "True"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["ALLOWED_HOSTS"] = "127.0.0.1,localhost,testserver"
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.test"

    args = parser.parse_args()

    if not args.django and not args.style:
        # If no tests are specified, run both Django and Code Style tests
        django_tests()
        style_tests()
        _()
    else:
        if args.django:
            django_tests()
            _()
        if args.style:
            style_tests()
            _()


if __name__ == "__main__":
    main()
