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


import * as runtime from '../runtime';

/**
 *
 */
export class LoggedInApi extends runtime.BaseAPI {

    /**
     */
    async loggedInRetrieveRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/api/logged_in/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     */
    async loggedInRetrieve(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.loggedInRetrieveRaw(initOverrides);
    }

}
