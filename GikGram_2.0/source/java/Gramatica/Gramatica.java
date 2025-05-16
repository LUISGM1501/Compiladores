/*
 * Gramatica.java
 *
 * 2025/05/16 00:04:54
 *
 * Archivo generado por GikGram 2.0
 *
 * Copyright © Olminsky 2011 Derechos reservados
 * Reproducción sin fines de lucro permitida
 */

package Gramatica;

/**
 * Esta clase contiene:
 * - Constantes necesarias para el driver de parsing
 * - Constantes con las rutinas semánticas
 * - Y los métodos necesarios para el driver de parsing
 */
public abstract class Gramatica
{
	/* Esta es la única clase que se accede fuera del paquete Gramatica */

	/**
	 * Constante que contiene el código de familia del terminal de fin de archivo
	 */
	public static final int MARCA_DERECHA = 133;

	/**
	 * Constante que contiene el número del no-terminal inicial
	 * (el primer no-terminal que aparece en la gramática)
	 */
	public static final int NO_TERMINAL_INICIAL = 134;

	/**
	 * Constante que contiene el número máximo de columnas que tiene los lados derechos
	 */
	public static final int MAX_LADO_DER = 9;

	/**
	 * Constante que contiene el número máximo de follows
	 */
	public static final int MAX_FOLLOWS = 48;

	/* Constantes con las rutinas semánticas */
	public static final int init_tsg = 217;
	public static final int free_tsg = 218;
	public static final int chk_func_start = 219;
	public static final int chk_func_return = 220;
	public static final int sw1 = 221;
	public static final int sw3 = 222;
	public static final int sw2 = 223;
	public static final int check_is_procedure = 224;

	/**
	 * Método esTerminal
			Devuelve true si el símbolo es un terminal
			o false de lo contrario
	 * @param numSimbolo
			Número de símbolo
	 */
	public static final boolean esTerminal(int numSimbolo)
	{
		return ((0 <= numSimbolo) && (numSimbolo <= 133));
	}

	/**
	 * Método esNoTerminal
			Devuelve true si el símbolo es un no-terminal
			o false de lo contrario
	 * @param numSimbolo
			Número de símbolo
	 */
	public static final boolean esNoTerminal(int numSimbolo)
	{
		return ((134 <= numSimbolo) && (numSimbolo <= 216));
	}

	/**
	 * Método esSimboloSemantico
			Devuelve true si el símbolo es un símbolo semántico
			(incluyendo los símbolos de generación de código)
			o false de lo contrario
	 * @param numSimbolo
			Número de símbolo
	 */
	public static final boolean esSimboloSemantico(int numSimbolo)
	{
		return ((217 <= numSimbolo) && (numSimbolo <= 224));
	}

	/**
	 * Método getTablaParsing
			Devuelve el número de regla contenida en la tabla de parsing
	 * @param numNoTerminal
			Número del no-terminal
	 * @param numTerminal
			Número del terminal
	 */
	public static final int getTablaParsing(int numNoTerminal, int numTerminal)
	{
		return GTablaParsing.getTablaParsing(numNoTerminal, numTerminal);
	}

	/**
	 * Método getLadosDerechos
			Obtiene un símbolo del lado derecho de la regla
	 * @param numRegla
			Número de regla
	 * @param numColumna
			Número de columna
	 */
	public static final int getLadosDerechos(int numRegla, int numColumna)
	{
		return GLadosDerechos.getLadosDerechos(numRegla, numColumna);
	}

	/**
	 * Método getNombresTerminales
			Obtiene el nombre del terminal
	 * @param numTerminal
			Número del terminal
	 */
	public static final String getNombresTerminales(int numTerminal)
	{
		return GNombresTerminales.getNombresTerminales(numTerminal);
	}

	/**
	 * Método getTablaFollows
			Obtiene el número de terminal del follow del no-terminal
	 * @param numNoTerminal
			Número de no-terminal
	 * @param numColumna
			Número de columna
	 */
	public static final int getTablaFollows(int numNoTerminal, int numColumna)
	{
		return GTablaFollows.getTablaFollows(numNoTerminal, numColumna);
	}
}
