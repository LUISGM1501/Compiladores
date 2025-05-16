/*
 * Gramatica.java
 *
 * 2025/05/16 00:04:54
 *
 * Archivo generado por GikGram 2.0
 *
 * Copyright � Olminsky 2011 Derechos reservados
 * Reproducci�n sin fines de lucro permitida
 */

package Gramatica;

/**
 * Esta clase contiene:
 * - Constantes necesarias para el driver de parsing
 * - Constantes con las rutinas sem�nticas
 * - Y los m�todos necesarios para el driver de parsing
 */
public abstract class Gramatica
{
	/* Esta es la �nica clase que se accede fuera del paquete Gramatica */

	/**
	 * Constante que contiene el c�digo de familia del terminal de fin de archivo
	 */
	public static final int MARCA_DERECHA = 133;

	/**
	 * Constante que contiene el n�mero del no-terminal inicial
	 * (el primer no-terminal que aparece en la gram�tica)
	 */
	public static final int NO_TERMINAL_INICIAL = 134;

	/**
	 * Constante que contiene el n�mero m�ximo de columnas que tiene los lados derechos
	 */
	public static final int MAX_LADO_DER = 9;

	/**
	 * Constante que contiene el n�mero m�ximo de follows
	 */
	public static final int MAX_FOLLOWS = 48;

	/* Constantes con las rutinas sem�nticas */
	public static final int init_tsg = 217;
	public static final int free_tsg = 218;
	public static final int chk_func_start = 219;
	public static final int chk_func_return = 220;
	public static final int sw1 = 221;
	public static final int sw3 = 222;
	public static final int sw2 = 223;
	public static final int check_is_procedure = 224;

	/**
	 * M�todo esTerminal
			Devuelve true si el s�mbolo es un terminal
			o false de lo contrario
	 * @param numSimbolo
			N�mero de s�mbolo
	 */
	public static final boolean esTerminal(int numSimbolo)
	{
		return ((0 <= numSimbolo) && (numSimbolo <= 133));
	}

	/**
	 * M�todo esNoTerminal
			Devuelve true si el s�mbolo es un no-terminal
			o false de lo contrario
	 * @param numSimbolo
			N�mero de s�mbolo
	 */
	public static final boolean esNoTerminal(int numSimbolo)
	{
		return ((134 <= numSimbolo) && (numSimbolo <= 216));
	}

	/**
	 * M�todo esSimboloSemantico
			Devuelve true si el s�mbolo es un s�mbolo sem�ntico
			(incluyendo los s�mbolos de generaci�n de c�digo)
			o false de lo contrario
	 * @param numSimbolo
			N�mero de s�mbolo
	 */
	public static final boolean esSimboloSemantico(int numSimbolo)
	{
		return ((217 <= numSimbolo) && (numSimbolo <= 224));
	}

	/**
	 * M�todo getTablaParsing
			Devuelve el n�mero de regla contenida en la tabla de parsing
	 * @param numNoTerminal
			N�mero del no-terminal
	 * @param numTerminal
			N�mero del terminal
	 */
	public static final int getTablaParsing(int numNoTerminal, int numTerminal)
	{
		return GTablaParsing.getTablaParsing(numNoTerminal, numTerminal);
	}

	/**
	 * M�todo getLadosDerechos
			Obtiene un s�mbolo del lado derecho de la regla
	 * @param numRegla
			N�mero de regla
	 * @param numColumna
			N�mero de columna
	 */
	public static final int getLadosDerechos(int numRegla, int numColumna)
	{
		return GLadosDerechos.getLadosDerechos(numRegla, numColumna);
	}

	/**
	 * M�todo getNombresTerminales
			Obtiene el nombre del terminal
	 * @param numTerminal
			N�mero del terminal
	 */
	public static final String getNombresTerminales(int numTerminal)
	{
		return GNombresTerminales.getNombresTerminales(numTerminal);
	}

	/**
	 * M�todo getTablaFollows
			Obtiene el n�mero de terminal del follow del no-terminal
	 * @param numNoTerminal
			N�mero de no-terminal
	 * @param numColumna
			N�mero de columna
	 */
	public static final int getTablaFollows(int numNoTerminal, int numColumna)
	{
		return GTablaFollows.getTablaFollows(numNoTerminal, numColumna);
	}
}
