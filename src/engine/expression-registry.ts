// Direct parameter mappings for fallback when native expression API fails
// These are the raw parameter values from the model's .exp3.json files
const expressionParams: Record<string, Record<string, number>> = {
  '笑眯眯': {
    ParamExpression_3: 1.0, ParamHide_EyesL1: 1.0,
    ParamHighLightHide_EyesL1: 1.0, ParamHide_EyeSocket: 1.0,
    ParamHide_EyeSocket2: 1.0, ParamExpression_1: 0.0,
    ParamExpression_2: 0.0, ParamExpression_4: 0.0,
  },
  '眯眯眼': {
    ParamExpression_4: 1.0, ParamHide_EyesL1: 1.0,
    ParamHighLightHide_EyesL1: 1.0, ParamHide_EyeSocket: 1.0,
    ParamHide_EyeSocket2: 1.0, ParamExpression_1: 0.0,
    ParamExpression_2: 0.0, ParamExpression_3: 0.0,
  },
  '泪珠': {
    ParamExpression_2: 1.0, ParamHide_EyesL1: 1.0,
    ParamHighLightHide_EyesL1: 1.0, ParamHide_EyeSocket: 1.0,
    ParamHide_EyeSocket2: 1.0, ParamExpression_1: 0.0,
    ParamExpression_3: 0.0, ParamExpression_4: 0.0,
  },
  '眼泪': {
    ParamExpression_1: 1.0, ParamExpression_2: 0.0,
    ParamExpression_3: 0.0, ParamExpression_4: 0.0,
  },
}

const normalParams: Record<string, number> = {
  ParamExpression_1: 0.0, ParamExpression_2: 0.0,
  ParamExpression_3: 0.0, ParamExpression_4: 0.0,
  ParamHide_EyesL1: 0.0, ParamHighLightHide_EyesL1: 0.0,
  ParamHide_EyeSocket: 0.0, ParamHide_EyeSocket2: 0.0,
}

export function getExpressionParams(name: string): Record<string, number> {
  if (!name || name === 'normal') return { ...normalParams }
  return expressionParams[name] ? { ...expressionParams[name] } : {}
}
