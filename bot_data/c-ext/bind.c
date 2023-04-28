#include "libpokestarbot.h"
char xp_at_docs[] = "Get the total experience at a level.";
char xp_for_docs[] = "Get the experience for a level from the previous level.";
char calculate_level_docs[] = "Get the level from raw experience.";

PyMethodDef pokestarbot_c_funcs[] = {
{"xp_at", (PyCFunction)xp_at, METH_VARARGS, xp_at_docs},
{"xp_for", (PyCFunction)xp_for, METH_VARARGS, xp_for_docs},
{"calculate_level", (PyCFunction)calculate_level, METH_VARARGS, calculate_level_docs},
{ NULL }
};

char pokestarbot_c_docs[] = "This is the C speedups for PokestarBot.";

PyModuleDef pokestarbot_c_mod = {
	PyModuleDef_HEAD_INIT,
	"pokestarbot_c",
	pokestarbot_c_docs,
	-1,
	pokestarbot_c_funcs,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_pokestarbot_c(void) {
	return PyModule_Create(&pokestarbot_c_mod);
}
