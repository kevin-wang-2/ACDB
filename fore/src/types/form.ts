export type FormValue = string | number | Date | boolean | boolean[];

export interface FormValidator {
    required?: boolean,
    message?: string,
    validator?: (rule: any, value: string, cb: Function) => void
}

export type FormValidatorGroup = FormValidator[];

export interface FormValidationTree {
    [key: string]: FormValidatorGroup
}

export interface Option {
    key: string;
    value: string | number;
    label?: string;
}
