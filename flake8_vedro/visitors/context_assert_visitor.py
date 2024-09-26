import ast
from typing import List, Optional, Type

from flake8_plugin_utils import Error

from flake8_vedro.abstract_checkers import ContextChecker
from flake8_vedro.config import Config
from flake8_vedro.types import StepType
from flake8_vedro.visitors._visitor_with_filename import VisitorWithFilename


class Context:
    def __init__(self, context_node: List[StepType], filename: str):
        self.context_node = context_node
        self.filename = filename


class ContextAssertVisitor(VisitorWithFilename):
    context_checkers: List[ContextChecker] = []

    def __init__(self, config: Optional[Config] = None,
                 filename: Optional[str] = None) -> None:
        super().__init__(config, filename)

    @property
    def config(self):
        return self._config

    @classmethod
    def register_context_checker(cls, checker: Type[ContextChecker]):
        cls.context_checkers.append(checker())
        return checker

    @classmethod
    def deregister_all(cls):
        cls.context_checkers = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> List[Error]:
        if self.config.is_context_assert_optional:
            return []
        else:
            for decorator in node.decorator_list:
                if (isinstance(decorator, ast.Attribute)
                        and decorator.value.id == 'vedro'
                        and decorator.attr == 'context'):
                    context = Context(context_node=node,
                                      filename=self.filename)
                    try:
                        for checker in self.context_checkers:
                            self.errors.extend(checker.check_context(context, self.config))
                    except Exception as e:
                        print(f'Linter failed: checking {context.filename} with {checker.__class__}.\n'
                              f'Exception: {e}')

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> List[Error]:
        if self.config.is_context_assert_optional:
            return []
        else:
            for decorator in node.decorator_list:
                if (isinstance(decorator, ast.Attribute)
                        and decorator.value.id == 'vedro'
                        and decorator.attr == 'context'):
                    context = Context(context_node=node,
                                      filename=self.filename)
                    try:
                        for checker in self.context_checkers:
                            self.errors.extend(checker.check_context(context, self.config))
                    except Exception as e:
                        print(f'Linter failed: checking {context.filename} with {checker.__class__}.\n'
                              f'Exception: {e}')
