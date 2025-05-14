/*
 * Gramatica.h
 *
 * 2025/05/13 20:48:49
 *
 * Archivo generado por GikGram 2.0
 *
 * Copyright © Olminsky 2011 Derechos reservados
 * Reproducción sin fines de lucro permitida
 */
#pragma once

#ifndef INC_Gramatica_h_
	#define INC_Gramatica_h_

	/* Constantes necesarias para un driver de parsing */
	#define TERMINAL(X)  ((0 <= (X)) && ((X) <= 133))
	#define NO_TERMINAL(X)  ((134 <= (X)) && ((X) <= 217))
	#define MARCA_DERECHA 133
	#define NO_TERMINAL_INICIAL 134
	#define MAX_LADO_DER 9

	/* Constantes con las rutinas semánticas */
	#define init_tsg 218
	#define free_tsg 219
	#define chk_no_redeclare 220
	#define chk_func_start 221
	#define chk_func_return 222
	#define sw1 223
	#define sw3 224
	#define sw2 225
	#define check_is_procedure 226

	/* Prototipos de las tablas */
	extern const int TablaParsing[84][NO_TERMINAL_INICIAL];
	extern const int LadosDerechos[222][MAX_LADO_DER];

#endif /* INC_Gramatica_h_ */
