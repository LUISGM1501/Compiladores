/*
 * GNombresTerminales.java
 *
 * 2025/05/28 17:11:05
 *
 * Archivo generado por GikGram 2.0
 *
 * Copyright © Olminsky 2011 Derechos reservados
 * Reproducción sin fines de lucro permitida
 */

package Gramatica;

/**
 * Esta clase contiene los nombres de los terminales
 * y los métodos necesarios para acceder a ella
 */
abstract class GNombresTerminales
{
	/**
	 * Contiene los nombres de los terminales
	 */
	private static final String[] NombresTerminales =
	{
		"WORLD_NAME",
		"BEDROCK",
		"RESOURCE_PACK",
		"INVENTORY",
		"RECIPE",
		"CRAFTING_TABLE",
		"SPAWN_POINT",
		"OBSIDIAN",
		"ANVIL",
		"WORLD_SAVE",
		"STACK",
		"RUNE",
		"SPIDER",
		"TORCH",
		"CHEST",
		"BOOK",
		"GHAST",
		"SHELF",
		"ENTITY",
		"REF",
		"ON",
		"OFF",
		"POLLO_CRUDO",
		"POLLO_ASADO",
		"REPEATER",
		"CRAFT",
		"TARGET",
		"HIT",
		"MISS",
		"JUKEBOX",
		"DISC",
		"SILENCE",
		"SPAWNER",
		"EXHAUSTED",
		"WALK",
		"SET",
		"TO",
		"STEP",
		"WITHER",
		"CREEPER",
		"ENDER_PEARL",
		"RAGEQUIT",
		"SPELL",
		"RITUAL",
		"RESPAWN",
		"IS_ENGRAVED",
		"IS_INSCRIBED",
		"ETCH_UP",
		"ETCH_DOWN",
		"AND",
		"OR",
		"NOT",
		"XOR",
		"BIND",
		"HASH",
		"FROM",
		"EXCEPT",
		"SEEK",
		"ADD",
		"DROP",
		"FEED",
		"MAP",
		"BIOM",
		"VOID",
		"UNLOCK",
		"LOCK",
		"MAKE",
		"GATHER",
		"FORGE",
		"TAG",
		"IS",
		"IS_NOT",
		"HOPPER_STACK",
		"HOPPER_RUNE",
		"HOPPER_SPIDER",
		"HOPPER_TORCH",
		"HOPPER_CHEST",
		"HOPPER_GHAST",
		"DROPPER_STACK",
		"DROPPER_RUNE",
		"DROPPER_SPIDER",
		"DROPPER_TORCH",
		"DROPPER_CHEST",
		"DROPPER_GHAST",
		"CHUNK",
		"SOULSAND",
		"MAGMA",
		"NUMERO_ENTERO",
		"NUMERO_DECIMAL",
		"CADENA",
		"CARACTER",
		"IDENTIFICADOR",
		"DOBLE_IGUAL",
		"MENOR_QUE",
		"MAYOR_QUE",
		"MENOR_IGUAL",
		"MAYOR_IGUAL",
		"IGUAL",
		"SUMA",
		"RESTA",
		"MULTIPLICACION",
		"DIVISION",
		"MODULO",
		"PARENTESIS_ABRE",
		"PARENTESIS_CIERRA",
		"CORCHETE_ABRE",
		"CORCHETE_CIERRA",
		"LLAVE_ABRE",
		"LLAVE_CIERRA",
		"PUNTO_Y_COMA",
		"COMA",
		"PUNTO",
		"DOS_PUNTOS",
		"ARROBA",
		"BARRA",
		"FLECHA",
		"SUMA_IGUAL",
		"RESTA_IGUAL",
		"MULTIPLICACION_IGUAL",
		"DIVISION_IGUAL",
		"MODULO_IGUAL",
		"RETURN",
		"SUMA_FLOTANTE",
		"RESTA_FLOTANTE",
		"MULTIPLICACION_FLOTANTE",
		"DIVISION_FLOTANTE",
		"MODULO_FLOTANTE",
		"SUMA_FLOTANTE_IGUAL",
		"RESTA_FLOTANTE_IGUAL",
		"MULTIPLICACION_FLOTANTE_IGUAL",
		"DIVISION_FLOTANTE_IGUAL",
		"MODULO_FLOTANTE_IGUAL",
		"COERCION",
		" EOF "
	};

	/**
	 * Método getNombresTerminales
			Obtiene el nombre del terminal
	 * @param numTerminal
			Número del terminal
	 */
	static final String getNombresTerminales(int numTerminal)
	{
		return NombresTerminales[numTerminal];
	}
}
