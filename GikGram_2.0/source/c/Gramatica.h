/*
 * Gramatica.h
 *
 * 2025/05/11 13:08:11
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
	#define NO_TERMINAL(X)  ((134 <= (X)) && ((X) <= 211))
	#define MARCA_DERECHA 133
	#define NO_TERMINAL_INICIAL 134
	#define MAX_LADO_DER 9

	/* Constantes con las rutinas semánticas */
	/* NO SE DETECTARON SÍMBOLOS SEMÁNTICOS EN LA GRAMÁTICA */

	/* Prototipos de las tablas */
	extern const int TablaParsing[78][NO_TERMINAL_INICIAL];
	extern const int LadosDerechos[219][MAX_LADO_DER];

#endif /* INC_Gramatica_h_ */
