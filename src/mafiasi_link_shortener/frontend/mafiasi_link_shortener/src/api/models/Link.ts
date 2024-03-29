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
 * @interface Link
 */
export interface Link {
    /**
     *
     * @type {string}
     * @memberof Link
     */
    readonly selflink: string;
    /**
     *
     * @type {string}
     * @memberof Link
     */
    _short?: string;
    /**
     *
     * @type {string}
     * @memberof Link
     */
    readonly shortlink: string;
    /**
     * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
     * @type {string}
     * @memberof Link
     */
    readonly owner: string;
    /**
     *
     * @type {string}
     * @memberof Link
     */
    target: string;
    /**
     *
     * @type {boolean}
     * @memberof Link
     */
    loginRequired?: boolean;
}

/**
 * Check if a given object implements the Link interface.
 */
export function instanceOfLink(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "selflink" in value;
    isInstance = isInstance && "shortlink" in value;
    isInstance = isInstance && "owner" in value;
    isInstance = isInstance && "target" in value;

    return isInstance;
}

export function LinkFromJSON(json: any): Link {
    return LinkFromJSONTyped(json, false);
}

export function LinkFromJSONTyped(json: any, ignoreDiscriminator: boolean): Link {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {

        'selflink': json['selflink'],
        '_short': !exists(json, 'short') ? undefined : json['short'],
        'shortlink': json['shortlink'],
        'owner': json['owner'],
        'target': json['target'],
        'loginRequired': !exists(json, 'login_required') ? undefined : json['login_required'],
    };
}

export function LinkToJSON(value?: Link | null): any {
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
