declare module '../Devscript/interpreter/interpretertry' {
    export class Environment {
        constructor();
        execute_calculation(syntax_name: string, ...args: any[]): any;
    }

    export class Tokenizer {
        constructor(source_code: string);
        tokenize(): any[];
    }

    export class Parser {
        constructor(tokens: any[]);
        parse_all_syntax(): any;
    }

    export class DevScriptAutocomplete {
        constructor(registry: any);
        get_suggestions(prefix: string): Record<string, any>;
        get_signature(func_name: string): string;
        get_param_suggestions(func_name: string, param_name: string): any[];
    }

    export class DevScriptInterpreter {
        registry: any;
        constructor();
        suggest_completion(current_text: string, cursor_position: number): Record<string, any>;
    }

    export function evaluate_code(source_code: string): any;
    export function run_script(code: string): any;
}
