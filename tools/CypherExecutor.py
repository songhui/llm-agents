from typing import List
from autogen.coding import CodeBlock, CodeResult, CodeExtractor, MarkdownCodeExtractor, CodeExecutor
from IPython import get_ipython

from tools.neo4j import cypher # THIS IMPORT IS USED BY %%CYPHER! DO NOT DELETE IT!

class CypherCodeExecutor(CodeExecutor):
    """
    It extends a code executor to run cypher queries.
    This changes only the way a code block is executed, it will encapsulate the 
    code block with a run query function to be run in a jupyter environment.
    This is done because cypher execution is not supported by autogen, otherwise python 
    and jupyter are.
    """
    
    @property
    def code_extractor(self) -> CodeExtractor:
        # Extract code from markdown blocks.
        return MarkdownCodeExtractor()

    def __init__(self) -> None:
        # Get the current IPython instance running in this notebook.
        self._ipython = get_ipython()

    def execute_code_blocks(self, code_blocks: List[CodeBlock]) -> CodeResult:
        """
        This is the real customization to make an agent execute code.
        When we use %%cypher we are calling an Ipython magic that will call run_query. 
        Run_query will then run the function on the neo4j database using the neo4j driver.

        Args:
            code_blocks (List[CodeBlock]): The code blocks created by the coder agent.

        Returns:
            CodeResult: The result is the code output and the exit code (0 or 1).
        """
        log = ""

        for code_block in code_blocks:
            result = self._ipython.run_cell("%%cypher \n" + code_block.code)

            if result.result:
                log += str(result.result)
            exitcode = 0 if result.success else 1
            if result.error_before_exec:
                log += f"\n{result.error_before_exec}"
                exitcode = 1
            if result.error_in_exec:
                log += f"\n{result.error_in_exec}"
                exitcode = 1

            if exitcode != 0:
                break

        return CodeResult(exit_code=exitcode, output=log)