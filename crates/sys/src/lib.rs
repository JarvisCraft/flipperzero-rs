//! Low-level bindings for the Flipper Zero.

#![no_std]

pub mod furi;

#[allow(non_upper_case_globals)]
#[allow(non_camel_case_types)]
#[allow(non_snake_case)]
mod bindings;

/// Create a static C string.
/// Will automatically add a NUL terminator.
#[macro_export]
macro_rules! c_string {
    ($str:literal $(,)?) => {{
        concat!($str, "\0").as_ptr() as *const core::ffi::c_char
    }};
}

/// Crash the system.
#[macro_export]
macro_rules! crash {
    ($msg:literal $(,)?) => {
        unsafe {
            // Crash message is passed via r12
            let msg = $crate::c_string!($msg);
            core::arch::asm!("", in("r12") msg, options(nomem, nostack));

            $crate::__furi_crash();
            // `unreachable!` generates exception machinery, `noreturn` does not
            core::arch::asm!("", options(noreturn));
        }
    };
}

/// Re-export bindings
pub use bindings::*;
