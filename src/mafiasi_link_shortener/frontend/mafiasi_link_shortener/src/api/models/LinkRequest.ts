/* tslint:disable */
/* eslint-disable */
/**
 * Mafiasi Link Shortener
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * Contact: ag-server@informatik.uni-hamburg.de
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 *
 * @export
 * @interface LinkRequest
 */
export interface LinkRequest {
    /**
     *
     * @type {string}
     * @memberof LinkRequest
     */
    _short?: string;
    /**
     *
     * @type {string}
     * @memberof LinkRequest
     */
    target: string;
    /**
     *
     * @type {boolean}
     * @memberof LinkRequest
     */
    loginRequired?: boolean;
}

/**
 * Check if a given object implements the LinkRequest interface.
 */
export function instanceOfLinkRequest(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "target" in value;

    return isInstance;
}

export function LinkRequestFromJSON(json: any): LinkRequest {
    return LinkRequestFromJSONTyped(json, false);
}

export function LinkRequestFromJSONTyped(json: any, ignoreDiscriminator: boolean): LinkRequest {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {

        '_short': !exists(json, 'short') ? undefined : json['short'],
        'target': json['target'],
        'loginRequired': !exists(json, 'login_required') ? undefined : json['login_required'],
    };
}

export function LinkRequestToJSON(value?: LinkRequest | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {

        'short': value._short,
        'target': value.target,
        'login_required': value.loginRequired,
    };
}
