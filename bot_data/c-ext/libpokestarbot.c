#include <stdio.h>
#include <Python.h>
#include "libpokestarbot.h"
#include "libminecraftxp.h"

PyObject * calculate_level(PyObject *self, PyObject *args) {
	unsigned long long num;

	if(!PyArg_ParseTuple(args, "K", &num)){
		return NULL;
	}

	unsigned long long result;

    Py_BEGIN_ALLOW_THREADS

	result = calculate_level_inner(num);

	Py_END_ALLOW_THREADS

	return Py_BuildValue("K", result);
}

PyObject * xp_at(PyObject *self, PyObject *args) {
	unsigned long long num;

	if(!PyArg_ParseTuple(args, "K", &num)){
		return NULL;
	}

	unsigned long long result = xp_at_inner(num);

	return Py_BuildValue("K", result);
}


PyObject * xp_for(PyObject *self, PyObject *args) {
	unsigned long long num;

	if(!PyArg_ParseTuple(args, "K", &num)){
		return NULL;
	}

    if (num == 0){
    return Py_BuildValue("K", 0);
    }
	unsigned long long result = xp_for_inner(num);

	return Py_BuildValue("K", result);
}
