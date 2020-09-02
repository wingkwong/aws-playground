#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { MskStack } from '../lib/msk-stack';

const app = new cdk.App();
const awsConfig = {
    env: {        
        region: process.env.CDK_DEFAULT_REGION,
        account: process.env.CDK_DEFAULT_ACCOUNT,
    }
};
new MskStack(app, 'MskStack', awsConfig);
