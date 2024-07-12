
import os
import sys
import importlib.util


try:
    location = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pipes')
    spec = importlib.util.spec_from_file_location("pipes", os.path.join(location, '__init__.py'))
    pipes = importlib.util.module_from_spec(spec)
    sys.modules['pipes'] = pipes
    spec.loader.exec_module(pipes)

    from pipes.cli import main
    main.main()

except ModuleNotFoundError:
    print('----------------------------------------------------------------')
    print(f"NREL pipes CLI package not loaded - {location}")
    print('----------------------------------------------------------------\n')
