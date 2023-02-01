# **Expectation Suite Name**: `suite_ds_tr_proy_ano`
# In[1]:

import great_expectations as ge
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.data_context.types.resource_identifiers import ExpectationSuiteIdentifier
from great_expectations.exceptions import DataContextError

context = ge.data_context.DataContext()


# Feel free to change the name of your suite here. Renaming this will not remove the other one.
table_name = "inv_cierr_inv"
expectation_suite_name = "suite_ds_"+table_name
try:
    suite = context.get_expectation_suite(expectation_suite_name=expectation_suite_name)
    print(f'Loaded ExpectationSuite "{suite.expectation_suite_name}" containing {len(suite.expectations)} expectations.')
except DataContextError:
    suite = context.create_expectation_suite(expectation_suite_name=expectation_suite_name)
    print(f'Created ExpectationSuite "{suite.expectation_suite_name}".')


# ## Create & Edit Expectations
#
#
# You are adding Expectation configurations to the suite. Since you selected manual mode, there is no sample batch of data and no validation happens during this process. See our documentation for more info and examples: **[How to create a new Expectation Suite without a sample batch](https://docs.greatexpectations.io/docs/guides/expectations/how_to_create_and_edit_expectations_based_on_domain_knowledge_without_inspecting_data_directly)**.
#
# Note that if you do use interactive mode you may specify a sample batch of data to use when creating your Expectation Suite. You can then use a `validator` to get immediate feedback on your Expectations against your specified sample batch.
#
#
# You can see all the available expectations in the **[expectation gallery](https://greatexpectations.io/expectations)**.

# ### Table Expectation(s)

# No table level expectations are in this suite. Feel free to add some here.
#

# ### Column Expectation(s)

# No column level expectations are in this suite. Feel free to add some here.
#

# In[2]:
expectation_configuration = ExpectationConfiguration(
   expectation_type="expect_column_values_to_not_be_null",
   kwargs={
      "column": "codigo_unico"
   },
   meta={
      "notes": {
         "format": "markdown",
         "content": "El campo CODIGO_UNICO no acepta valores nulos"
      }
   }
)
suite.add_expectation(expectation_configuration=expectation_configuration)


# In[7]:
expectation_configuration = ExpectationConfiguration(
   expectation_type="expect_column_values_to_not_be_null",
   kwargs={
      "column": "id_cierre"
   },
   meta={
      "notes": {
         "format": "markdown",
         "content": "El campo ID_CIERRE no acepta valores nulos"
      }
   }
)
suite.add_expectation(expectation_configuration=expectation_configuration)
# In[8]:
expectation_configuration = ExpectationConfiguration(
   expectation_type="expect_column_values_to_not_be_null",
   kwargs={
      "column": "cod_snip"
   },
   meta={
      "notes": {
         "format": "markdown",
         "content":  "El campo COD_SNIP no acepta valores nulos"
      }
   }
)
suite.add_expectation(expectation_configuration=expectation_configuration)

# In[8]:
expectation_configuration = ExpectationConfiguration(
   expectation_type="expect_column_values_to_not_be_null",
   kwargs={
      "column": "id_estado"
   },
   meta={
      "notes": {
         "format": "markdown",
         "content": "El campo ID_ESTADO no acepta valores nulos"
      }
   }
)
suite.add_expectation(expectation_configuration=expectation_configuration)

# In[8]:
expectation_configuration = ExpectationConfiguration(
   expectation_type="expect_column_values_to_be_between",
   kwargs={
      "column": "id_estado",
      "max_value": 1,
      "min_value": 0
   },
   meta={
      "notes": {
         "format": "markdown",
         "content": "El campo ID_ESTADO acepta valores {0,1}}"
      }
   }
)
suite.add_expectation(expectation_configuration=expectation_configuration)

# In[8]:
expectation_configuration = ExpectationConfiguration(
   expectation_type="expect_column_values_to_be_between",
   kwargs={
      "column": "flg_activo",
      "max_value": 1,
      "min_value": 0
   },
   meta={
      "notes": {
         "format": "markdown",
         "content": "El campo FLG_ACTIVO acepta valores {0,1}}"
      }
   }
)
suite.add_expectation(expectation_configuration=expectation_configuration)



# ## Review & Save Your Expectations
#
# Let's save the expectation suite as a JSON file in the `great_expectations/expectations` directory of your project.
#
# Let's now rebuild your Data Docs, which helps you communicate about your data with both machines and humans.

# In[5]:
print(context.get_expectation_suite(expectation_suite_name=expectation_suite_name))
context.save_expectation_suite(expectation_suite=suite, expectation_suite_name=expectation_suite_name)

suite_identifier = ExpectationSuiteIdentifier(expectation_suite_name=expectation_suite_name)
context.build_data_docs(resource_identifiers=[suite_identifier])
context.open_data_docs(resource_identifier=suite_identifier)