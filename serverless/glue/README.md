# Glue

## Examine the schemas in the data catalog

Create a DynamicFrame object using a catalog database
```py
dynamicFrameObj = glueContext.create_dynamic_frame.from_catalog(
             database="THE_DATABASE_TO_READ_FROM",
             table_name="THE_TABLE_NAME_TO_READ_FROM")
print "Count: ", dynamicFrameObj.count()
dynamicFrameObj.printSchema()
```

## Filter the data

Use ``toDF()`` to convert a DynamicFrame object to an Apache Spark DataFrame object.
```py
dynamicFrameObj = dynamicFrameObj.drop_fields(['FIELD_1_TO_BE_DROPPED','FIELD_2_TO_BE_DROPPED'])
            .rename_field('ORIGINAL_FIELD_NAME_1', 'NEW_FIELD_NAME_1')
            .rename_field('ORIGINAL_FIELD_NAME_2', 'NEW_FIELD_NAME_2')
dynamicFrameObj.toDF().show()
```

## Select the field

```py
dynamicFrameObj.select_fields(['FIELD_TO_BE_SELECTED']).toDF().distinct().show()
```

## Simple Joining 

```py
dynamicFrameObj = Join.apply(dynamicFrameObj1, dynamicFrameObj2, 'DYNAMICFRAME_OBJ_ID_1','DYNAMICFRAME_OBJ_ID_2')
                        .drop_fields(['fielFIELD_1_TO_BE_DROPPEDd_1', 'FIELD_2_TO_BE_DROPPED'])
print "Count: ", dynamicFrameObj.count()
dynamicFrameObj.printSchema()
```

## S3 Bucket Name Prefix  

Start with ``aws-glue*`` prefix for Glue to access the buckets using the preconfigured ``AWSGlueServiceRole`` IAM role. 

```json
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Action":[
            "glue:*",
            "s3:GetBucketLocation",
            "s3:ListBucket",
            "s3:ListAllMyBuckets",
            "s3:GetBucketAcl"
         ],
         "Resource":[
            "*"
         ]
      },
      {
         "Effect":"Allow",
         "Action":[
            "s3:CreateBucket"
         ],
         "Resource":[
            "arn:aws:s3:::aws-glue-*"
         ]
      },
      {
         "Effect":"Allow",
         "Action":[
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject"
         ],
         "Resource":[
            "arn:aws:s3:::aws-glue-*/*",
            "arn:aws:s3:::*/*aws-glue-*/*"
         ]
      },
      {
         "Effect":"Allow",
         "Action":[
            "s3:GetObject"
         ],
         "Resource":[
            "arn:aws:s3:::crawler-public*",
            "arn:aws:s3:::aws-glue-*"
         ]
      }
   ]
}
```

## Enabling the Spark UI 

- To create a development endpoint with the Spark UI enabled
- Sign in to the AWS Management Console and open the AWS Glue console at https://console.aws.amazon.com/glue/.
- In the navigation pane, choose Dev endpoints.
- Choose Add endpoint.
- In Configuration, open the Spark UI options.
- In the Spark UI tab, choose Enable.
- Specify an Amazon S3 path for storing the Spark event logs.