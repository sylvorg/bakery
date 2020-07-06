# From Imports
from addict import Dict as D
from functools import partial
from gensing import tea, frosting
from itertools import chain
from nanite import (
	check_type,
	module_installed,
	fullpath,
	mixinport,
)
from os import environ
from typing import (
	List,
	Tuple,
	Dict,
	MutableSequence as MS,
	Any,
	Generator,
	Union,
)

mixins: Generator[str, None, None] = (fullpath(f"{mixin}.py", f_back = 2) for mixin in (
	"_create_command",
	"_funky_properties",
	"_long_property_vars",
	"_process_args_kwargs",
	"_return_output",
	"_run_frosting",
	"_set",
	"_short_property_vars",
	"baking_",
))

class _milcery(*(mixinport(mixins))):

	"""
		Answer: https://stackoverflow.com/questions/26315584/apply-a-function-to-all-instances-of-a-class/26315625#26315625
		User: https://stackoverflow.com/users/625914/behzad-nouri
	"""

	def __init__(
		self,
		program: str,
		*args,
		_ignore_check: bool = False,
		_baked_commands: Dict[str, Any] = D({}),
		_baked_settings: Dict[str, Any] = D({}),
		_ = 0,
		**kwargs,
	):
		"""
			_type can be any type, such as:
			* iter
			* list
			* tuple
			* set
			* frozenset

			A good way to debug commands is to see what the command actually was, using the "_str"
			keyword argument.
		"""
		self.program: str = program
		self._ignore_check: bool = _ignore_check

		self._command = D({})
		self._command.baked = _baked_commands
		
		self._settings = D({})
		self._settings.baked = _baked_settings

		self._sub = D({})

		"""

		"""
		self._settings.defaults: Dict[str, Any] = {
			"_type": iter,
			"_capture": "stdout",
			"_shell": False,
			"_frosting": False,
			"_str": False,
			"_ignore_stderr": False,
			"_verbosity": int(
				environ.get("verbose_bakery", 0)
			),
			"_run_as": "",
			"_n_lines": D(
				{
					"ordinal": "first",
					"number": None,
					"std": "out",
				}
			),
			"_kwarg_one_dash": False,
			"_fixed_key": False,
			"_print": False,
			"_tiered": False,

			# If set to "verbosity", this setting will trigger a verbose return with as much
			# information as dictated by the "_verbosity" setting;
			# otherwise, this will trigger a regular return, returning just one category, such as
			# standard out, standard error, etc.
			"_return": "verbosity",


			# This setting will use a single forward slash instead of a dash for options
			"_dos": False,

		}
		self._settings.functions = (
			"frosting_",
			"f_",
			"shell_",
			"str_",
		)

		self._shells: List[str] = [
			"zsh",
			"bash",
			"sh",
			"fish",
			"xonsh",
			"elvish",
			"tcsh",
			"powershell",
			"cmd",
		]
		self._shell = (
			True if self.program in self._shells else False
		)

		# Returns the default allowed types and adds "str" as well
		self._allowed_type_names: List[str] = check_type(
			lst=True
		) + ["str"]

		self._captures: Tuple[str] = (
			"stdout",
			"stderr",
			"both",
			"run",
		)
		
		self._return_categories: Tuple[str] = (
			"stdout",
			"stderr",
			"return_code",
			"return_codes",
			"command",
			"args",
			"kwargs",
			"gensing",
			"verbosity",
		)

		sa = kwargs.pop("_starter_args", [])
		sa = [sa] if isinstance(sa, (str, bytes, bytearray)) else list(sa)
		ska = kwargs.pop("_starter_kwargs", dict())
		if _:
			print(1)
			self._args = sa
			self._kwargs = ska
			self._sub.unprocessed = "command"
			self._set_and_process(*args, **kwargs)
			return self._return_frosted_output()
		else:
			self._args = list(args) + list(sa)
			kwargs.update(ska)
			self._kwargs = kwargs

	# DONE: Something's wrong with this, or returning the generator created by this
	# DONE: Always remember a generator is used up
	def _convert_to_generator(self, input):
		yield from input

	def _convert_to_type(self, input, _type):
		if _type.__name__ == "str":
			return " ".join(input)
		if _type.__name__ in ("generator", "iter"):
			return self._convert_to_generator(input)
		else:
			return _type(input)

    def _subcommand_check(self, subcommand):
	    if subcommand in self._settings.functions:
	        self._sub.unprocessed = "command"
        else:
			self._sub.unprocessed = subcommand
			self._sub.processed = subcommand.replace("_", "-")

	def __getattr__(self, subcommand):
		def inner(*args, **kwargs):
		    self._subcommand_check(subcommand)
			self._set_and_process(*args, **kwargs)
			return self._return_frosted_output()
		return inner

	def _return_frosted_output(self):
		# DONE: Change to account for the new return methods
		if isinstance(output := self._run_frosting(
			_subcommand = self._sub.unprocessed,
		), (dict, tea, frosting)):
			return frosting(output, self._capture)
		else:
			# DONE: _convert_to_type isn't working here because _run_frosting resets
			# all properties, including _type; find an alternative
			return self._convert_to_type(frosting(output), type(output))

	def _set_and_process(self, *args, **kwargs):

		self._set(_setup = True)

		set_with_sub = partial(self._set, _subcommand = self._sub.unprocessed)

		self._args, self._kwargs = set_with_sub(
			*self._args,
			_calling = True,
			**self._kwargs,
		)

		args, kwargs = set_with_sub(
			*args,
			_calling = True,
			**kwargs,
		)

		set_with_sub(
			_final = True,
		)

		set_with_sub(
			_apply = True,
		)
		
		process_with_sub = partial(
			self._process_args_kwargs,
			_subcommand = self._sub.unprocessed,
		)

		process_with_sub(
			*self._args,
			_calling = True,
			_starter_regular = "starter",
			**self._kwargs,
		)
		
		process_with_sub(
			*args,
			_calling = True,
			_starter_regular = "regular",
			**kwargs,
		)
		
		process_with_sub(
			_final = True,
		)

	def add_types_(self, *args):
		self._allowed_type_names = self._allowed_type_names + list(args)

	def add_shells_(self, *args):
		self._shells = self._shells + list(args)

	def __deepcopy__(self):
		return self.__class__(
			program,
			_baked_commands = D(self._command.baked),
			_baked_settings = D(self._settings.baked),
		)

	def __iter__(self):
		self.n = 0

		# TODO: Change to account for the new return methods
		if isinstance(output := self._run_frosting(
			_subcommand = self._sub.unprocessed,
		), (dict, tea, frosting)):
			self.__next_output = list(getattr(
				output,
				"stderr" if self._capture == "stderr" else "stdout"
			))
		else:
			self.__next_output = list(output)

		return self

	def __next__(self):
		if self.n < len(self.__next_output):
			self.n += 1
			return self.__next_output[self.n - 1]
		else:
			raise StopIteration
