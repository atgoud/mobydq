/*Connect to database*/
\connect mobydq



/*Create table indicator*/
CREATE TABLE base.indicator (
    id SERIAL PRIMARY KEY
  , name TEXT NOT NULL UNIQUE
  , description TEXT
  , execution_order INTEGER DEFAULT 0
  , flag_active BOOLEAN DEFAULT FALSE
  , created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  , created_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , updated_by_id INTEGER DEFAULT base.get_current_user_id() REFERENCES base.user(id)
  , user_group_id INTEGER DEFAULT 0 REFERENCES base.user_group(id)
  , indicator_group_id INTEGER NOT NULL REFERENCES base.indicator_group(id)
  , indicator_type_id INTEGER NOT NULL REFERENCES base.indicator_type(id)
);

COMMENT ON TABLE base.indicator IS
'Indicators compute data sets on one or several data sources in order to evaluate the quality of their data.';

CREATE TRIGGER indicator_update_updated_date BEFORE UPDATE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_date();

CREATE TRIGGER indicator_update_updated_by_id BEFORE UPDATE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.update_updated_by_id();

CREATE TRIGGER indicator_delete_parameter BEFORE DELETE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('parameter', 'indicator_id');

CREATE TRIGGER indicator_delete_session BEFORE DELETE
ON base.indicator FOR EACH ROW EXECUTE PROCEDURE
base.delete_children('session', 'indicator_id');



/*Create function to duplicate an indicator*/
CREATE OR REPLACE FUNCTION base.duplicate_indicator(indicator_id INTEGER, new_indicator_name TEXT)
RETURNS base.indicator AS $$
#variable_conflict use_variable
DECLARE
    indicator base.indicator;
BEGIN
    -- Duplicate indicator
    INSERT INTO base.indicator (name, description, execution_order, flag_active, indicator_type_id, indicator_group_id, user_group_id)
    SELECT new_indicator_name, a.description, a.execution_order, a.flag_active, a.indicator_type_id, a.indicator_group_id, a.user_group_id
    FROM base.indicator a
    WHERE a.id=indicator_id
    RETURNING * INTO indicator;

    -- Duplicate parameters
    INSERT INTO base.parameter (value, parameter_type_id, indicator_id, user_group_id)
    SELECT a.value, a.parameter_type_id, indicator.id, a.user_group_id
    FROM base.parameter a
    WHERE a.indicator_id=indicator_id;

    RETURN indicator;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

COMMENT ON FUNCTION base.duplicate_indicator IS
'Function used to duplicate an indicator.';
