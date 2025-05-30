/*
 * Gramatica.java
 *
 * 2025/05/30 02:31:22
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
	public static final int MAX_LADO_DER = 14;

	/**
	 * Constante que contiene el número máximo de follows
	 */
	public static final int MAX_FOLLOWS = 48;

	/* Constantes con las rutinas semánticas */
	public static final int init_tsg = 221;
	public static final int free_tsg = 222;
	public static final int chk_const_existence = 223;
	public static final int add_const_symbol = 224;
	public static final int chk_type_existence = 225;
	public static final int start_type_def = 226;
	public static final int end_type_def = 227;
	public static final int add_type_symbol = 228;
	public static final int save_current_type = 229;
	public static final int chk_var_existence = 230;
	public static final int add_var_symbol = 231;
	public static final int mark_var_initialized = 232;
	public static final int default_uninitialized = 233;
	public static final int create_tsl = 234;
	public static final int free_tsl = 235;
	public static final int chk_func_start = 236;
	public static final int set_in_function = 237;
	public static final int save_func_name = 238;
	public static final int chk_func_return = 239;
	public static final int unset_in_function = 240;
	public static final int chk_file_literal = 241;
	public static final int chk_in_loop = 242;
	public static final int chk_return_context = 243;
	public static final int mark_has_return = 244;
	public static final int chk_dead_code = 245;
	public static final int chk_file_expr = 246;
	public static final int chk_label_unique = 247;
	public static final int add_label = 248;
	public static final int chk_label_exists = 249;
	public static final int mark_label_used = 250;
	public static final int process_chunk = 251;
	public static final int chk_bool_expr = 252;
	public static final int chk_no_nested_else = 253;
	public static final int no_else = 254;
	public static final int enter_loop = 255;
	public static final int exit_loop = 256;
	public static final int chk_for_var = 257;
	public static final int chk_for_expr = 258;
	public static final int chk_step_expr = 259;
	public static final int default_step_one = 260;
	public static final int sw1 = 261;
	public static final int save_switch_type = 262;
	public static final int sw3 = 263;
	public static final int chk_case_type = 264;
	public static final int sw2 = 265;
	public static final int chk_with_var = 266;
	public static final int enter_with_scope = 267;
	public static final int exit_with_scope = 268;
	public static final int chk_lvalue_modifiable = 269;
	public static final int push_lvalue_type = 270;
	public static final int chk_assignment_types = 271;
	public static final int chk_float_assign_op = 272;
	public static final int chk_int_assign_op = 273;
	public static final int chk_etch_up_args = 274;
	public static final int chk_etch_down_args = 275;
	public static final int chk_is_engraved_args = 276;
	public static final int chk_is_inscribed_args = 277;
	public static final int chk_hash_args = 278;
	public static final int chk_bind_args = 279;
	public static final int chk_from_args = 280;
	public static final int chk_except_args = 281;
	public static final int chk_seek_args = 282;
	public static final int chk_add_args = 283;
	public static final int chk_drop_args = 284;
	public static final int chk_feed_args = 285;
	public static final int chk_map_args = 286;
	public static final int chk_biom_args = 287;
	public static final int chk_void_args = 288;
	public static final int push_bool_type = 289;
	public static final int chk_bool_ops = 290;
	public static final int push_type = 291;
	public static final int pop_two_push_result = 292;
	public static final int chk_div_zero = 293;
	public static final int push_float_type = 294;
	public static final int chk_float_ops = 295;
	public static final int chk_unary_types = 296;
	public static final int apply_coercion = 297;
	public static final int push_unary_plus = 298;
	public static final int push_unary_minus = 299;
	public static final int push_unary_not = 300;
	public static final int chk_func_exists = 301;
	public static final int chk_recursion = 302;
	public static final int chk_func_params = 303;
	public static final int chk_dropper_stack_args = 304;
	public static final int chk_dropper_rune_args = 305;
	public static final int chk_dropper_spider_args = 306;
	public static final int chk_dropper_torch_args = 307;
	public static final int chk_dropper_chest_args = 308;
	public static final int chk_dropper_ghast_args = 309;
	public static final int chk_hopper_stack_args = 310;
	public static final int chk_hopper_rune_args = 311;
	public static final int chk_hopper_spider_args = 312;
	public static final int chk_hopper_torch_args = 313;
	public static final int chk_hopper_chest_args = 314;
	public static final int chk_hopper_ghast_args = 315;
	public static final int count_arg = 316;
	public static final int no_args = 317;
	public static final int check_arg_count = 318;
	public static final int chk_id_exists = 319;
	public static final int chk_var_initialized = 320;
	public static final int chk_array_access = 321;
	public static final int chk_record_access = 322;
	public static final int process_param_group = 323;
	public static final int no_params = 324;
	public static final int save_param_type = 325;
	public static final int add_param_symbol = 326;
	public static final int process_ref_type = 327;
	public static final int start_array_literal = 328;
	public static final int end_array_literal = 329;
	public static final int start_record_literal = 330;
	public static final int end_record_literal = 331;
	public static final int push_int_type = 332;
	public static final int push_string_type = 333;
	public static final int push_char_type = 334;
	public static final int chk_return_in_function = 335;
	public static final int chk_return_in_procedure = 336;

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
		return ((134 <= numSimbolo) && (numSimbolo <= 220));
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
		return ((221 <= numSimbolo) && (numSimbolo <= 336));
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
