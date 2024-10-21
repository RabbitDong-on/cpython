This is Python 2.7.3, modified to be run in a Chef environment.

All Chef-related additions are Copyright (c) EPFL 2014 and distributed under the MIT license.  See the file "LICENSE" for the general Python license terms.
  

## Setting up the Chef environment for Python

The guest setup for running Python programs with Chef is mostly automated by the ``chef/Makefile.interp`` file, which prepares a Python virtualenv configured with instrumented Python interpreters at various symbolic optimization levels.

We assume the following project structure in the guest:

    $CHEF_ROOT
      - python-src (the Python code base -- this tree)
        - chef
          - build (does not exist, you need to create it).


### Phase 1: Preparing the guest environment ("kvm" mode in S2E)

This phase should run in normal (KVM) mode in S2E. Consult the main Chef README file for more details.

In the ``$CHEF_ROOT/python-src/chef/build``, run the following:

    $ make -f ../Makefile.interp

Then activate the resulting Python environment using:

    $ source $CHEF_ROOT/python-src/chef/build/python-env/bin/activate

Next, install the Chef native extension:

    $ cd $CHEF_ROOT/python-src/chef/pychef && pip install -e .


### Phase 2: Preparing the symbolic environment ("prep" mode in S2E)

Activate the Python environment:

    $ source $CHEF_ROOT/python-src/chef/build/python-env/bin/activate

Enable symbolic execution mode:

    $ export PYTHONSYMBEX=1

(Optional) The environment includes all the optimization configurations used in the paper.  To select a particular optimization, set the "PYTHONSYMBEXOPT" environment variable before invoking the Python executable:

    $ PYTHONSYMBEXOPT=0 python -c 'print "hi"'

The optimization numbers go from 0 (no optimizations) to 4 (all optimizations) -- see the next section for more details.


### Phase 3: Symbolic Execution (the "sym" mode in S2E)

Run the target symbolic test case. For instance:

    $ python symtests/asplos_tests.py ArgparseTest


## Building a Chef-adapted Python binary

Behind the scenes, Makefile.interp builds the Python interpreter under a set of predefined configurations.  For more flexibility, you can manually configure & build the interpreter, as follows.

Configure with symbolic execution and optimizations enabled:

    $ ./configure [--enable-symbex] [--enable-symbex-opt[=OPT[,OPT[,...]]]] [--prefix=<path>] ...

where ``OPT`` can be one of the following:

  * ``none``: No optimization enabled (equivalent to ``PYTHONSYMBEXOPT=0``)
  * ``concrbuff``: Memory buffer concretization (equivalent to ``PYTHONSYMBEXOPT=1``)
  * ``intern``: Interning elimination (available when ``PYTHONSYMBEXOPT=2``)
  * ``hashes``: Everything above + Hash neutralization (available when ``PYTHONSYMBEXOPT=3``)
  * ``fastpath``: Everything above + Fast path elimination (available when ``PYTHONSYMBEXOPT=3``)
  * ``all``: All optimizations enabled (available when ``PYTHONSYMBEXOPT=4`` or empty)

Then build as normal (``make && make install``).

When the ``--enable-symbex`` flag is set during configuration, the resulting Python binary receives an additional ``-Y`` flag which activates the dynamic instrumentation.  Alternatively, the same can be achieved by setting the ``PYTHONSYMBEX`` environment variable.
