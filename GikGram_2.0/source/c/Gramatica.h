/*
 * Gramatica.h
 *
 * 2025/05/30 02:31:22
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
	#define NO_TERMINAL(X)  ((134 <= (X)) && ((X) <= 220))
	#define MARCA_DERECHA 133
	#define NO_TERMINAL_INICIAL 134
	#define MAX_LADO_DER 14

	/* Constantes con las rutinas semánticas */
	#define init_tsg 221
	#define free_tsg 222
	#define chk_const_existence 223
	#define add_const_symbol 224
	#define chk_type_existence 225
	#define start_type_def 226
	#define end_type_def 227
	#define add_type_symbol 228
	#define save_current_type 229
	#define chk_var_existence 230
	#define add_var_symbol 231
	#define mark_var_initialized 232
	#define default_uninitialized 233
	#define create_tsl 234
	#define free_tsl 235
	#define chk_func_start 236
	#define set_in_function 237
	#define save_func_name 238
	#define chk_func_return 239
	#define unset_in_function 240
	#define chk_file_literal 241
	#define chk_in_loop 242
	#define chk_return_context 243
	#define mark_has_return 244
	#define chk_dead_code 245
	#define chk_file_expr 246
	#define chk_label_unique 247
	#define add_label 248
	#define chk_label_exists 249
	#define mark_label_used 250
	#define process_chunk 251
	#define chk_bool_expr 252
	#define chk_no_nested_else 253
	#define no_else 254
	#define enter_loop 255
	#define exit_loop 256
	#define chk_for_var 257
	#define chk_for_expr 258
	#define chk_step_expr 259
	#define default_step_one 260
	#define sw1 261
	#define save_switch_type 262
	#define sw3 263
	#define chk_case_type 264
	#define sw2 265
	#define chk_with_var 266
	#define enter_with_scope 267
	#define exit_with_scope 268
	#define chk_lvalue_modifiable 269
	#define push_lvalue_type 270
	#define chk_assignment_types 271
	#define chk_float_assign_op 272
	#define chk_int_assign_op 273
	#define chk_etch_up_args 274
	#define chk_etch_down_args 275
	#define chk_is_engraved_args 276
	#define chk_is_inscribed_args 277
	#define chk_hash_args 278
	#define chk_bind_args 279
	#define chk_from_args 280
	#define chk_except_args 281
	#define chk_seek_args 282
	#define chk_add_args 283
	#define chk_drop_args 284
	#define chk_feed_args 285
	#define chk_map_args 286
	#define chk_biom_args 287
	#define chk_void_args 288
	#define push_bool_type 289
	#define chk_bool_ops 290
	#define push_type 291
	#define pop_two_push_result 292
	#define chk_div_zero 293
	#define push_float_type 294
	#define chk_float_ops 295
	#define chk_unary_types 296
	#define apply_coercion 297
	#define push_unary_plus 298
	#define push_unary_minus 299
	#define push_unary_not 300
	#define chk_func_exists 301
	#define chk_recursion 302
	#define chk_func_params 303
	#define chk_dropper_stack_args 304
	#define chk_dropper_rune_args 305
	#define chk_dropper_spider_args 306
	#define chk_dropper_torch_args 307
	#define chk_dropper_chest_args 308
	#define chk_dropper_ghast_args 309
	#define chk_hopper_stack_args 310
	#define chk_hopper_rune_args 311
	#define chk_hopper_spider_args 312
	#define chk_hopper_torch_args 313
	#define chk_hopper_chest_args 314
	#define chk_hopper_ghast_args 315
	#define count_arg 316
	#define no_args 317
	#define check_arg_count 318
	#define chk_id_exists 319
	#define chk_var_initialized 320
	#define chk_array_access 321
	#define chk_record_access 322
	#define process_param_group 323
	#define no_params 324
	#define save_param_type 325
	#define add_param_symbol 326
	#define process_ref_type 327
	#define start_array_literal 328
	#define end_array_literal 329
	#define start_record_literal 330
	#define end_record_literal 331
	#define push_int_type 332
	#define push_string_type 333
	#define push_char_type 334
	#define chk_return_in_function 335
	#define chk_return_in_procedure 336

	/* Prototipos de las tablas */
	extern const int TablaParsing[87][NO_TERMINAL_INICIAL];
	extern const int LadosDerechos[233][MAX_LADO_DER];

#endif /* INC_Gramatica_h_ */
